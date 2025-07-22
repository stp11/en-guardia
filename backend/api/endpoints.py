from database import get_session
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from models import Episode
from sqlmodel import Session, select

router = APIRouter()


@router.get("/episodes", tags=["episodis"], response_model=Page[Episode])
def get_episodes(session: Session = Depends(get_session)):
    query = select(Episode).order_by(Episode.published_at.desc())
    return paginate(session, query)
