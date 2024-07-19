import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_app.main import app
from fastapi_app.src.database.models import Base
from fastapi_app.src.database.db import get_db
from fastapi_app.src.conf.config import settings
from fastapi_app.src.database.models import User

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    

@pytest.fixture(scope="module")
def user():
    return {"username": "testuser1", "email": "testuser1@example.com", "password": "Testuser!2"}


@pytest.fixture(scope="module")
def create_test_user(session, user):
    db_user = User(
        username=user['username'],
        email=user['email'],
        hashed_password=user['password']
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

