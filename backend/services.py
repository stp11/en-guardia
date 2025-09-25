import json
from datetime import datetime

from logger import logger
from models import Episode
from openai import OpenAI
from prompts import classification_prompt
from repositories import ICategoriesRepository, IEpisodesRepository
from sqlalchemy import Select


class EpisodesService:
    def __init__(self, episodes_repository: IEpisodesRepository):
        self.episodes_repository = episodes_repository

    def get_episodes_query(self, search: str | None, order: str) -> Select:
        """
        Orchestrates fetching the episodes query from the repository.
        Business logic would go here.
        """
        return self.episodes_repository.get_episodes_query(
            search=search, order=order
        )

    def create_episode_from_api_data(self, data: dict) -> Episode:
        """Maps API data dictionary to an Episode object."""
        return Episode(
            id=data["id"],
            title=data.get("titol"),
            slug=data.get("nom_friendly"),
            description=data.get("entradeta"),
            published_at=(
                self._parse_date(data["data_publicacio"])
                if data.get("data_publicacio")
                else None
            ),
        )

    def _parse_date(self, date_str: str) -> datetime:
        """Parse API date format: '09/09/2001 00:01:00'"""
        return datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")


class ClassificationService:
    def __init__(
        self,
        openai_client: OpenAI,
        episodes_repository: IEpisodesRepository,
        categories_repository: ICategoriesRepository,
    ):
        self.openai_client = openai_client
        self.episodes_repository = episodes_repository
        self.categories_repository = categories_repository

    def classify_episode(self, episode: Episode) -> dict | None:
        """Classify a single episode using OpenAI."""
        existing_categories = self.categories_repository.get_all_categories()
        existing_categories_list = [
            category.name for category in existing_categories
        ]
        prompt = classification_prompt(episode, existing_categories_list)

        logger.info(f"Prompt: {prompt}")

        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        logger.info(f"Classification response: {response}")
        try:
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Classification result: {result}")
            return result
        except Exception as e:
            logger.error(
                f"Failed to fetch classification from LLM for episode {episode.id}: {e}"  # noqa: E501
            )
            return None

    def save_categories_to_episode(
        self, episode: Episode, classification: dict | None
    ) -> None:
        """Save classified categories to the database."""
        all_categories = []

        if classification is None:
            logger.info(f"No classification found for episode {episode.id}")
            return

        try:
            for items in classification.values():
                logger.info(f"Saving categories: {items}")
                for item in items:
                    category = (
                        self.categories_repository.get_or_create_category(item)
                    )
                    logger.info(f"Saved category: {category}")
                    all_categories.append(category)
        except Exception as e:
            logger.error(f"Failed to save categories: {e}")
            return

        for category in all_categories:
            logger.info(
                f"Linking episode {episode.id} to category {category.id}"
            )
            self.episodes_repository.link_episode_to_category(
                episode.id, category.id
            )
        logger.info(
            f"Linked episode {episode.id} to categories {all_categories}"
        )
