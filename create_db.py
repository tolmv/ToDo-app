from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Параметры подключения к базе данных
DATABASE_URL = "postgresql://postgres:Your_password@localhost:5432/todo_db"

# Создание базы данных и таблиц
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")

class UserTodoPermission(Base):
    __tablename__ = "user_todo_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    todo_id = Column(Integer, ForeignKey("todos.id"))
    can_read = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)

# Создание движка подключения
engine = create_engine(DATABASE_URL)

# Создание всех таблиц
Base.metadata.create_all(bind=engine)

print("Таблицы успешно созданы!")
inspector = inspect(engine)

tables = inspector.get_table_names()

# Определите ожидаемые таблицы
expected_tables = {"users", "todos", "user_todo_permissions"}

# Проверьте, что все ожидаемые таблицы существуют
missing_tables = expected_tables - set(tables)

if not missing_tables:
    print("Все таблицы успешно созданы.")
else:
    print("Не удалось найти следующие таблицы:", missing_tables)
