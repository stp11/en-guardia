from datetime import datetime, timezone

from sqlmodel import TEXT, Column, DateTime, Field, SQLModel


class Episode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    slug: str | None = None
    description: str | None = Field(default=None, sa_column=Column(TEXT))
    published_at: datetime | None = Field(default=None, index=True)


class IngestionPosition(SQLModel, table=True):
    id: int | None = Field(default=1, primary_key=True)
    last_episode_id: int | None = None
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime, onupdate=datetime.now(timezone.utc)),
    )
