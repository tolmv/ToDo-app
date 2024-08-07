from sqlalchemy import create_engine
from models import Base, user

DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(DATABASE_URL)

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

