import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

PGUSER = os.environ.get("PGUSER")
PGPASSWORD = os.environ.get("PGPASSWORD")
PGHOST = os.environ.get("PGHOST")
PGPORT = os.environ.get("PGPORT", "5432")
PGDATABASE = os.environ.get("PGDATABASE")

DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"  # noqa: E501

is_debug = os.environ.get("BUILD_ENVIRONMENT") == "local"

engine = create_engine(DATABASE_URL, echo=is_debug, hide_parameters=True)

SessionLocal = sessionmaker(autocommit=False, bind=engine, class_=Session)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
