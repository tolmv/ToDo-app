from sqlalchemy.orm import Session
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.models.todo import Todo
from app.models.todo import UserTodoPermission
from app.db.database import get_db, engine, Base

# Убедитесь, что ваша база данных и таблицы созданы для тестов
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    yield Session(bind=engine)
    Base.metadata.drop_all(bind=engine)


import pytest
from sqlalchemy.orm import Session
from app.models.user import User

@pytest.fixture(scope="function")
def create_user(db_session: Session) -> User:
    user = User(username="testuser", hashed_password="fakehashedpassword")
    try:
        db_session.add(user)
        db_session.commit()
    except Exception:
        db_session.rollback()
        user = db_session.query(User).filter_by(username="testuser").first()
        if not user:
            raise
    return user


@pytest.fixture(scope="function")
def db_session(db: Session):
    session = db
    yield session
    session.rollback()

@pytest.fixture(scope="function")
def client():
    return TestClient(app)

@pytest.fixture(scope="function")
def create_user(db_session: Session) -> User:
    user = User(username="testuser", hashed_password="fakehashedpassword")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def create_todo(db_session: Session, create_user: User) -> Todo:
    todo = Todo(title="Test Todo", description="Test Description", owner_id=create_user.id)
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

def test_create_todo(client: TestClient, create_user: User):
    response = client.post(
        "/todos",
        json={"title": "New Todo", "description": "New Description"},
        headers={"Authorization": f"Bearer {create_user.id}"}
    )
    assert response.status_code == 200

def test_read_todo(client: TestClient, create_todo: Todo):
    response = client.get(f"/todos/{create_todo.id}", headers={"Authorization": f"Bearer {create_todo.owner_id}"})
    assert response.status_code == 200

def test_update_todo(client: TestClient, create_todo: Todo):
    response = client.put(
        f"/todos/{create_todo.id}",
        json={"title": "Updated Todo", "description": "Updated Description"},
        headers={"Authorization": f"Bearer {create_todo.owner_id}"}
    )
    assert response.status_code == 200

def test_delete_todo(client: TestClient, create_todo: Todo):
    response = client.delete(f"/todos/{create_todo.id}", headers={"Authorization": f"Bearer {create_todo.owner_id}"})
    assert response.status_code == 200

def test_create_todo_permission(client: TestClient, create_user: User, create_todo: Todo):
    response = client.post(
        f"/todos/{create_todo.id}/permissions",
        json={"user_id": create_user.id, "can_read": True, "can_update": True},
        headers={"Authorization": f"Bearer {create_todo.owner_id}"}
    )
    assert response.status_code == 200
