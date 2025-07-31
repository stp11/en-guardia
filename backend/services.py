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
