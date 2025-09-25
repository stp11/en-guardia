from database import get_session
from dependencies import get_episodes_service
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from models import EpisodeWithCategories
from services import EpisodesService
from sqlmodel import Session

router = APIRouter()


@router.get(
    "/episodes", tags=["episodis"], response_model=Page[EpisodeWithCategories]
)
def get_episodes(
    service: EpisodesService = Depends(get_episodes_service),
    # We still need the session for the pagination function
    session: Session = Depends(get_session),
    search: str = "",
    order: str = "desc",
):
    query = service.get_episodes_query(search=search, order=order)
    return paginate(session, query)
