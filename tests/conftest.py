import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.db.database import Base
from app.models.user import User
from app.models.todo import Todo
from app.models.todo import UserTodoPermission

DATABASE_URL = "postgresql://postgres:Your_password@localhost/todo_db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Session:
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        # Roll back any changes
        session.rollback()
        # Close the session
        session.close()
        # Drop the database tables
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    from fastapi.testclient import TestClient
    from app.main import app  # Import your FastAPI app here
    return TestClient(app)

@pytest.fixture(scope="function")
def create_user(db_session: Session):
    user = User(username="testuser", hashed_password="fakehashedpassword")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def create_todo(create_user: User, db_session: Session):
    todo = Todo(title="Test Todo", description="Test Description", owner_id=create_user.id)
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo
