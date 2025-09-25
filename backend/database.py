import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa: E501

is_debug = os.environ.get("BUILD_ENVIRONMENT") == "local"

engine = create_engine(DATABASE_URL, echo=is_debug, hide_parameters=True)

SessionLocal = sessionmaker(autocommit=False, bind=engine, class_=Session)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
