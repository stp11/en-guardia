from database import get_session
from fastapi import Depends
from repositories import EpisodesRepository, IEpisodesRepository
from services import EpisodesService
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
