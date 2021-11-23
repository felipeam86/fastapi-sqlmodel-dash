import pandas as pd
from sqlmodel import SQLModel, create_engine

sql_url = "postgresql://root:root@localhost:5432/sales"
engine = create_engine(sql_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def pandas_query(sql):
    with engine.connect() as conn:
        df = pd.read_sql(sql, con=conn)

    return df
