import json

import requests

from database import get_session
from logger import logger
from models import IngestionPosition

BASE_URL = (
    "https://api.3cat.cat/audios?programaradio_id=944&ordre=-data_publicacio"
)


def ingest_data():
    """
    Ingests episode data from a paginated API.

    Handles initial bulk ingestion and subsequent incremental updates.
    It processes pages until it finds an episode
    that has already been ingested, then stops.

    It uses the IngestionPosition model to track the last episode id
    and the total number of episodes ingested.
    """
    logger.info("Starting episode ingestion task.")

    with next(get_session()) as session:
        from repositories import EpisodesRepository
        from services import EpisodesService

        episodes_repository = EpisodesRepository(session)
        episodes_service = EpisodesService(episodes_repository)

        position = session.get(IngestionPosition, 1) or IngestionPosition(id=1)

        known_last_id = position.last_episode_id
        newest_id_this_run = None
        total_episodes_ingested = 0
        page = 1

        while True:
            url = f"{BASE_URL}&pagina={page}"
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                data = response.json().get("resposta", {})
                items = data.get("items", {}).get("item", [])

                if not items:
                    logger.info(f"No more items found on page {page}")
                    break

            except (
                requests.RequestException,
                json.JSONDecodeError,
                KeyError,
            ) as e:
                logger.error(f"Failed to fetch or parse page {page}: {e}")
                break  # Stop the process on any critical error

            episodes_to_add = []
            stop_processing = False

            for ep_data in items:
                if newest_id_this_run is None:
                    newest_id_this_run = ep_data["id"]

                if ep_data["id"] == known_last_id:
                    stop_processing = True
                    break

                episodes_to_add.append(
                    episodes_service.create_episode_from_api_data(ep_data)
                )

            if episodes_to_add:
                for episode in episodes_to_add:
                    episodes_repository.save_episode(episode)
                total_episodes_ingested += len(episodes_to_add)

            if stop_processing:
                logger.info(
                    "Found last known episode. Ingestion is up-to-date."
                )
                break

            total_pages = data.get("paginacio", {}).get("total_pagines", 0)
            if page >= total_pages:
                logger.info("Reached the final page of the API.")
                break

            page += 1

        if newest_id_this_run and newest_id_this_run != known_last_id:
            position.last_episode_id = newest_id_this_run
            session.add(position)
            session.commit()
            logger.info(
                f"Successfully ingested {total_episodes_ingested} episodes. Last ID set to {newest_id_this_run}."  # noqa: E501
            )
        else:
            logger.info("No new episodes were ingested.")


if __name__ == "__main__":
    ingest_data()
