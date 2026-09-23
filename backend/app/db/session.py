from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_database_url, get_test_database_url


def create_db_engine(database_url: str | None = None):
    """รองรับ CON-TECH-01 และ SQLite ในหน่วยความจำสำหรับทดสอบ"""
    url = database_url or get_database_url()
    engine_kwargs = {}

    if url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    return create_engine(url, **engine_kwargs)


def create_session_factory(database_url: str | None = None):
    engine = create_db_engine(database_url or get_test_database_url())
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
