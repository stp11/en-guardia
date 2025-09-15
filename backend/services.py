from datetime import datetime

from models import Episode
from repositories import IEpisodesRepository
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
