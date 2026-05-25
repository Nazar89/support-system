import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    client.post("/users/register", json={
        "username": "admin_test",
        "email": "admin@test.com",
        "password": "admin123",
        "role": "admin"
    })
    resp = client.post("/auth/login", json={"username": "admin_test", "password": "admin123"})
    return resp.json()["access_token"]


@pytest.fixture
def user_token(client):
    client.post("/users/register", json={
        "username": "user_test",
        "email": "user@test.com",
        "password": "user123",
        "role": "user"
    })
    resp = client.post("/auth/login", json={"username": "user_test", "password": "user123"})
    return resp.json()["access_token"]


@pytest.fixture
def operator_token(client):
    client.post("/users/register", json={
        "username": "operator_test",
        "email": "operator@test.com",
        "password": "op123",
        "role": "operator"
    })
    resp = client.post("/auth/login", json={"username": "operator_test", "password": "op123"})
    return resp.json()["access_token"]


@pytest.fixture
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def user_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def operator_headers(operator_token):
    return {"Authorization": f"Bearer {operator_token}"}


@pytest.fixture
def sample_ticket(client, user_headers):
    resp = client.post("/tickets/", json={
        "title": "Test ticket",
        "description": "Test description"
    }, headers=user_headers)
    return resp.json()


@pytest.fixture
def sample_faq(client, admin_headers):
    resp = client.post("/faq/", json={
        "question": "Test question?",
        "answer": "Test answer."
    }, headers=admin_headers)
    return resp.json()