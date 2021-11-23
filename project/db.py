from sqlmodel import SQLModel, create_engine

sql_url = "postgresql://root:root@localhost:5432/sales"
engine = create_engine(sql_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
