import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session

import src.modules  # noqa: F401 -- registers all models with Base.metadata
from src.core.database import Base


@pytest.fixture(scope="session")
def test_database_url() -> str:
    load_dotenv()
    database_url = os.environ["TEST_DATABASE_URL"]
    parsed_url = make_url(database_url)

    if (
        parsed_url.drivername != "postgresql+psycopg"
        or parsed_url.database != "pets-e-commerce-test"
    ):
        raise RuntimeError("TEST_DATABASE_URL must point to the PostgreSQL test database")

    return database_url


@pytest.fixture(scope="session")
def test_engine(test_database_url: str) -> Iterator[Engine]:
    engine = create_engine(test_database_url)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def test_schema(test_engine: Engine) -> None:
    Base.metadata.create_all(test_engine)


@pytest.fixture()
def test_db_session(test_schema: None, test_engine: Engine) -> Iterator[Session]:
    with test_engine.connect() as connection:
        trasanction = connection.begin()
        try:
            with Session(
                bind=connection,
                join_transaction_mode="create_savepoint"
            ) as session:
                yield session
        finally:
            trasanction.rollback()