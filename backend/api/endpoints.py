from fastapi import APIRouter, Depends, HTTPException, Path, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import Session

from database import get_session
from dependencies import get_categories_service, get_episodes_service
from logger import logger
from models import Category, CategoryType, EpisodeWithCategories
from services import CategoriesService, EpisodesService

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
    categories: str = Query(
        "", description="Comma-separated list of category IDs"
    ),
):
    query = service.get_episodes_query(
        search=search, order=order, categories=categories
    )
    return paginate(session, query)


@router.get(
    "/episodes/{id}", tags=["episodis"], response_model=EpisodeWithCategories
)
def get_episode(
    id: int = Path(..., description="Episode ID"),
    service: EpisodesService = Depends(get_episodes_service),
):
    logger.info(f"Fetching episode with id: {id}")
    episode = service.get_episode_by_id(id)
    if not episode:
        logger.warning(f"Episode with id {id} not found in database")
        raise HTTPException(status_code=404, detail="Episode not found")
    logger.info(
        f"Successfully retrieved episode: {episode.id} - {episode.title}"
    )
    return episode


@router.get("/categories", tags=["categories"], response_model=Page[Category])
def get_categories(
    service: CategoriesService = Depends(get_categories_service),
    session: Session = Depends(get_session),
    type: CategoryType = Query("", description="Category type"),
):
    return paginate(session, service.get_categories_query(type=type))
