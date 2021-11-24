import os

from sqlmodel import SQLModel, create_engine

sql_url = os.environ.get("DATABASE_URL")
engine = create_engine(sql_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
