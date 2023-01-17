import pytest
import os

from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructures.database.main import Base
from app.infrastructures.fastapi.main import app


engine = create_engine(
    os.environ.get('DATABASE_URL')
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app=app) as client:
        yield client
