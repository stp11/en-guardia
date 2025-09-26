from datetime import datetime, timezone
from enum import Enum

from sqlmodel import TEXT, Column, DateTime, Field, Relationship, SQLModel


class EpisodeCategory(SQLModel, table=True):
    episode_id: int | None = Field(
        default=None, foreign_key="episode.id", primary_key=True
    )
    category_id: int | None = Field(
        default=None, foreign_key="category.id", primary_key=True
    )


class CategoryType(str, Enum):
    TOPIC = "topic"
    LOCATION = "location"
    CHARACTER = "character"
    TIME_PERIOD = "time_period"


class CategoryBase(SQLModel):
    id: int
    slug: str
    name: str
    type: CategoryType | None


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True)
    name: str = Field(index=True)
    type: CategoryType | None = Field(index=True)

    episodes: list["Episode"] = Relationship(
        back_populates="categories", link_model=EpisodeCategory
    )


class EpisodeBase(SQLModel):
    id: int
    title: str
    slug: str | None
    description: str | None
    published_at: datetime | None


class EpisodeWithCategories(EpisodeBase):
    categories: list[CategoryBase] = []


class Episode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str | None = None
    description: str | None = Field(default=None, sa_column=Column(TEXT))
    published_at: datetime | None = Field(default=None, index=True)

    categories: list[Category] = Relationship(
        back_populates="episodes", link_model=EpisodeCategory
    )


class IngestionPosition(SQLModel, table=True):
    id: int | None = Field(default=1, primary_key=True)
    last_episode_id: int | None = None
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime, onupdate=datetime.now(timezone.utc)),
    )
