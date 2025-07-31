from unittest.mock import MagicMock

from repositories import IEpisodesRepository
from services import EpisodesService


class TestEpisodesService:
    def setup_method(self):
        self.mock_repo = MagicMock(spec=IEpisodesRepository)
        self.service = EpisodesService(episodes_repository=self.mock_repo)

    def test_episodes_service_calls_repository(self):
        search_term = "test"
        order_direction = "desc"

        self.service.get_episodes_query(
            search=search_term, order=order_direction
        )

        self.mock_repo.get_episodes_query.assert_called_once_with(
            search=search_term, order=order_direction
        )
