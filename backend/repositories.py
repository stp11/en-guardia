from abc import ABC, abstractmethod

from models import Episode
from sqlalchemy import Select
from sqlmodel import Session, select


class IEpisodesRepository(ABC):
    @abstractmethod
    def get_episodes_query(self, search: str | None, order: str) -> Select:
        pass

    @abstractmethod
    def save_episode(self, episode: Episode) -> Episode:
        pass


class EpisodesRepository(IEpisodesRepository):
    def __init__(self, session: Session):
        self.db_session = session

    def get_episodes_query(self, search: str | None, order: str) -> Select:
        query = select(Episode)

        if search and search.strip():
            search_term = f"%{search.strip()}%"
            query = query.where(Episode.title.like(search_term))

        if order == "desc":
            query = query.order_by(Episode.published_at.desc())
        else:
            query = query.order_by(Episode.published_at.asc())

        return query

    def save_episode(self, episode: Episode) -> Episode:
        return self.db_session.merge(episode)
