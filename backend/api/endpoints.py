from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import Session

from database import get_session
from dependencies import get_categories_service, get_episodes_service
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


@router.get("/categories", tags=["categories"], response_model=Page[Category])
def get_categories(
    service: CategoriesService = Depends(get_categories_service),
    session: Session = Depends(get_session),
    type: CategoryType = Query("", description="Category type"),
):
    return paginate(session, service.get_categories_query(type=type))
