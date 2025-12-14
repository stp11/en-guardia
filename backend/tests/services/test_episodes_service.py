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
            search=search_term, order=order_direction, categories=[]
        )

    def test_episodes_service_calls_repository_with_categories(self):
        result = self.service._parse_categories(categories_str="1,2,3")
        assert result == [1, 2, 3]

    def test_episodes_service_get_episode_by_id(self):
        self.service.get_episode_by_id(id=1)
        self.mock_repo.get_episode_by_id.assert_called_once_with(1)
