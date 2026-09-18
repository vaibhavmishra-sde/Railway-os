"""Shared fixtures for the backend test suite.

Database isolation strategy
----------------------------
- Each test function receives a session backed by a **transaction that is
  rolled back** at the end of the test, so no data leaks between tests and
  the development database is never touched.
- The in-memory SQLite engine is created once per test session and all DDL
  is applied at that point.
- Override ``TEST_DATABASE_URL`` in the environment to run against a real
  PostgreSQL instance in CI.
"""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.main import create_app

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")


@pytest.fixture(scope="session")
def test_engine():
    """Create the test engine and apply DDL once for the whole test session."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {},
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    """Yield a transactional DB session rolled back after every test function."""
    connection = test_engine.connect()
    transaction = connection.begin()
    TestSession = sessionmaker(bind=connection)
    session = TestSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client() -> TestClient:
    """Return an isolated FastAPI test client for the RailwayOS application."""
    with TestClient(create_app()) as test_client:
        yield test_client
