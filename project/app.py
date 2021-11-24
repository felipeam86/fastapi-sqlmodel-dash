from typing import List, Optional

from fastapi import FastAPI
from sqlmodel import Session, select

from . import db
from .models import Customer, Employee, Sales, Territory

app = FastAPI()


@app.on_event("startup")
def on_startup():
    db.create_db_and_tables()


@app.get("/territory/{hero_id}", response_model=Territory, tags=["Territory"])
def get_territory(hero_id: int) -> Territory:
    with Session(db.engine) as session:
        territory = session.get(Territory, hero_id)
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


@app.get("/customer/{customer_id}", response_model=Customer, tags=["Customer"])
def get_employee(customer_id: int) -> Customer:
    with Session(db.engine) as session:
        customer = session.get(Customer, customer_id)
        return customer


@app.get("/customers/{territory_id}", response_model=List[Customer], tags=["Customer"])
def get_customers(territory_id: int) -> List[Customer]:
    with Session(db.engine) as session:
        customers = session.exec(
            select(Customer).where(Customer.territory_id == territory_id)
        ).all()
        return customers
