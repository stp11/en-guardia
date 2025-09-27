from database import get_session
from fastapi import Depends
from repositories import (CategoriesRepository, EpisodesRepository,
                          ICategoriesRepository, IEpisodesRepository)
from services import CategoriesService, EpisodesService
from sqlmodel import Session


def get_episodes_repository(
    session: Session = Depends(get_session),
) -> IEpisodesRepository:
    """Dependency provider for the EpisodesRepository."""
    return EpisodesRepository(session=session)


def get_episodes_service(
    repo: IEpisodesRepository = Depends(get_episodes_repository),
) -> EpisodesService:
    """Dependency provider for the EpisodesService."""
    return EpisodesService(episodes_repository=repo)


def get_categories_repository(
    session: Session = Depends(get_session),
) -> ICategoriesRepository:
    """Dependency provider for the CategoriesRepository."""
    return CategoriesRepository(session=session)


def get_categories_service(
    repo: ICategoriesRepository = Depends(get_categories_repository),
) -> CategoriesService:
    """Dependency provider for the CategoriesService."""
    return CategoriesService(categories_repository=repo)
