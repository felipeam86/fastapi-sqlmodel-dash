from sqlalchemy import func, select

from .models import Customer, Employee, Sales, Territory


def get_top_n_employees(continent: str, topn: int):
    query = (
        select(
            Territory.continent,
            Territory.country,
            Employee.id.label("employee_id"),
            Employee.name,
            Employee.created_at.label("employee_subscription_date"),
            func.sum(Sales.amount).label("total_sales"),
            func.count(Sales.id).label("number_of_sales"),
            func.avg(Sales.amount).label("average_sale_amount"),
            func.count(Sales.id).label("nb_sales"),
            func.min(Sales.date).label("first_sale"),
            func.max(Sales.date).label("last_sale"),
            (func.max(Sales.date) - func.min(Sales.date)).label("days_as_employee"),
        )
        .where(Territory.continent == continent)
        .select_from(Territory)
        .join(Employee)
        .select_from(Employee)
        .join(Sales)
        .group_by(
            Territory.continent,
            Territory.country,
            Employee.id,
            Employee.created_at,
        )
        .order_by(func.sum(Sales.amount).desc())
        .limit(topn)
    )

    return query


def get_top_100_customers(continent: str):
    query = (
        select(
            Territory.continent,
            Territory.country,
            Customer.id.label("customer_id"),
            Customer.name,
            Customer.created_at.label("customer_subscription_date"),
            func.sum(Sales.amount).label("total_purchases"),
            func.avg(Sales.amount).label("average_purchase_amount"),
            func.count(Sales.id).label("number_of_purchases"),
            func.min(Sales.date).label("first_purchase"),
            func.max(Sales.date).label("last_purchase"),
            (func.max(Sales.date) - func.min(Sales.date)).label("days_as_customer"),
            (
                (func.max(Sales.date) - func.min(Sales.date)) / func.count(Sales.id)
            ).label("avg_time_between_purchases"),
        )
        .where(Territory.continent == continent)
        .select_from(Territory)
        .join(Customer)
        .select_from(Customer)
        .join(Sales)
        .group_by(
            Territory.continent,
            Territory.country,
            Customer.id,
            Customer.name,
            Customer.created_at,
        )
        .order_by(func.sum(Sales.amount).desc())
        .limit(100)
    )

    return query
