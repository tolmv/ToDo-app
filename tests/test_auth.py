import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal, engine, Base
from app.models.user import User

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register(setup_db):
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    
    db = SessionLocal()
    user = db.query(User).filter(User.username == "testuser").first()
    assert user is not None
    assert user.username == "testuser"
    assert user.hashed_password is not None  

def test_register_existing_user(setup_db):
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/register", json={"username": "testuser", "password": "newpass"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login(setup_db):
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
"""
def test_login_invalid_credentials(setup_db):
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/login", json={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"
"""