from sqlalchemy import func, select

from .models import Employee, Sales, Territory


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
