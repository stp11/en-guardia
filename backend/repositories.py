from abc import ABC, abstractmethod

from models import Category, Episode, EpisodeCategory
from slugify import slugify
from sqlalchemy import Select
from sqlmodel import Session, select


class ICategoriesRepository(ABC):
    @abstractmethod
    def get_or_create_category(self, name: str) -> Category:
        pass


class CategoriesRepository(ICategoriesRepository):
    def __init__(self, session: Session):
        self.db_session = session

    def get_or_create_category(self, name: str) -> Category:
        slug = slugify(name)
        category = self.db_session.exec(
            select(Category).where(Category.slug == slug)
        ).first()

        if not category:
            category = Category(name=name, slug=slug)
            self.db_session.add(category)
            self.db_session.flush()

        return category


class IEpisodesRepository(ABC):
    @abstractmethod
    def get_episodes_query(self, search: str | None, order: str) -> Select:
        pass

    @abstractmethod
    def save_episode(self, episode: Episode) -> Episode:
        pass

    @abstractmethod
    def link_episode_to_category(
        self, episode_id: int, category_id: int
    ) -> None:
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

    def link_episode_to_category(
        self, episode_id: int, category_id: int
    ) -> None:
        existing = self.db_session.exec(
            select(EpisodeCategory).where(
                EpisodeCategory.episode_id == episode_id,
                EpisodeCategory.category_id == category_id,
            )
        ).first()

        if not existing:
            link = EpisodeCategory(
                episode_id=episode_id, category_id=category_id
            )
            self.db_session.add(link)
