from datetime import datetime
from typing import List

from fastapi import FastAPI, Query
from sqlmodel import Session, select

from . import db, queries
from .models import (
    Continent,
    Customer,
    CustomerOut,
    Employee,
    Sales,
    SalesCreate,
    Territory,
)

app = FastAPI(title="Sales API")


@app.on_event("startup")
def on_startup():
    db.create_db_and_tables()


@app.get("/territory/{territory_id}", response_model=Territory, tags=["Territory"])
def get_territory(territory_id: int) -> Territory:
    with Session(db.engine) as session:
        territory = session.get(Territory, territory_id)
        return territory


@app.get("/territories/", response_model=List[Territory], tags=["Territory"])
def get_territories() -> List[Territory]:
    with Session(db.engine) as session:
        territories = session.exec(select(Territory)).all()
        return territories


@app.get("/employee/{employee_id}", response_model=Employee, tags=["Employee"])
def get_employee(employee_id: int) -> Employee:
    with Session(db.engine) as session:
        employee = session.get(Employee, employee_id)
        return employee


@app.get("/employees/", response_model=List[Employee], tags=["Employee"])
def get_employees() -> List[Employee]:
    with Session(db.engine) as session:
        employees = session.exec(select(Employee)).all()
        return employees


@app.get("/customer/{customer_id}", response_model=CustomerOut, tags=["Customer"])
def get_employee(customer_id: int) -> Customer:
    with Session(db.engine) as session:
        customer = session.get(Customer, customer_id)
        customer = CustomerOut(
            last_purchases=customer.purchases[-10:],
            **customer.dict(),
        )
        return customer


@app.get("/customers/{territory_id}", response_model=List[Customer], tags=["Customer"])
def get_customers(
    territory_id: int,
    offset: int = 0,
    limit: int = Query(default=50, lte=50),
) -> List[Customer]:
    with Session(db.engine) as session:
        customers = session.exec(
            select(Customer)
            .where(Customer.territory_id == territory_id)
            .offset(offset)
            .limit(limit)
        ).all()
        return customers


@app.get("/topn_employees/{continent}/{n}", tags=["Employee"])
def get_customers(continent: Continent, n: int):

    query = queries.get_top_n_employees(continent, n)
    with Session(db.engine) as session:
        topn_empoyees = session.exec(query).all()
        return topn_empoyees


@app.get("/top100_customers/{continent}", tags=["Customer"])
def get_customers(continent: Continent):

    query = queries.get_top_100_customers(continent)
    with Session(db.engine) as session:
        top100_customers = session.exec(query).all()
        return top100_customers


@app.post("/sale", response_model=Sales, tags=["Sales"])
def add_sale(sale: SalesCreate):
    with Session(db.engine) as session:
        sale = Sales(
            customer_id=sale.customer_id,
            employee_id=sale.employee_id,
            amount=sale.amount,
            date=datetime.now(),
        )
        session.add(sale)
        session.commit()
        session.refresh(sale)
        return sale
