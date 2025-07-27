from database import get_session
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from models import Episode
from sqlmodel import Session, select

router = APIRouter()


@router.get("/episodes", tags=["episodis"], response_model=Page[Episode])
def get_episodes(session: Session = Depends(get_session), search: str = ""):
    query = select(Episode).order_by(Episode.published_at.desc())

    if search.strip():
        search_term = f"%{search.strip()}%"
        query = query.filter(Episode.title.like(search_term))

    return paginate(session, query)
