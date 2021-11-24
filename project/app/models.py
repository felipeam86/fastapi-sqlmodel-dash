from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Territory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    continent: str
    country: str
    created_at: datetime
    customers: List["Customer"] = Relationship(back_populates="territory")
    employees: List["Employee"] = Relationship(back_populates="territory")


class Human(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime
    territory_id: int = Field(foreign_key="territory.id")


class Employee(Human, table=True):
    territory: Territory = Relationship(back_populates="employees")
    sales: List["Sales"] = Relationship(back_populates="seller")


class Customer(Human, table=True):
    territory: Territory = Relationship(back_populates="customers")
    purchases: List["Sales"] = Relationship(back_populates="customer")


class CustomerOut(Human):
    last_purchases: List["Sales"]


class Sales(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    employee_id: int = Field(foreign_key="employee.id")
    date: datetime
    amount: float
    customer: Customer = Relationship(back_populates="purchases")
    seller: Employee = Relationship(back_populates="sales")


Territory.update_forward_refs()
Employee.update_forward_refs()
Customer.update_forward_refs()
CustomerOut.update_forward_refs()
