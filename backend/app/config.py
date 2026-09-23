import os
from functools import lru_cache


DEFAULT_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/booking"


@lru_cache(maxsize=1)
def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


@lru_cache(maxsize=1)
def get_test_database_url() -> str:
    return os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
