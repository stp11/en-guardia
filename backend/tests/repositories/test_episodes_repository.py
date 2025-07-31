from datetime import datetime

from models import Episode
from repositories import EpisodesRepository
from sqlmodel import Session


class TestEpisodesRepository:
    def setup_method(self):
        self.episodes = [
            Episode(
                id=1,
                title="Episodi sobre Grecia",
                published_at=datetime(2025, 1, 1),
            ),
            Episode(
                id=2,
                title="Episodi sobre la Guerra Civil",
                published_at=datetime(2025, 1, 2),
            ),
            Episode(
                id=3,
                title="Episodi sobre la Guerra del Vietnam",
                published_at=datetime(2025, 1, 3),
            ),
        ]

    def test_repository_search(self, db_session: Session):
        db_session.add_all(self.episodes)
        db_session.commit()
        repo = EpisodesRepository(session=db_session)

        query = repo.get_episodes_query(search="Guerra", order="asc")
        results = db_session.exec(query).all()

        assert len(results) == 2
        assert results[0].title == "Episodi sobre la Guerra Civil"
        assert results[1].title == "Episodi sobre la Guerra del Vietnam"

    def test_repository_ordering(self, db_session: Session):
        db_session.add_all(self.episodes)
        db_session.commit()
        repo = EpisodesRepository(session=db_session)

        query_desc = repo.get_episodes_query(search=None, order="desc")
        results_desc = db_session.exec(query_desc).all()

        query_asc = repo.get_episodes_query(search=None, order="asc")
        results_asc = db_session.exec(query_asc).all()

        assert results_desc[0].title == "Episodi sobre la Guerra del Vietnam"
        assert results_asc[0].title == "Episodi sobre Grecia"
