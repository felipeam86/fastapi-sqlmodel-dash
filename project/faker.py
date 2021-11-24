from datetime import datetime, timedelta
from random import randint, random, seed
from typing import Dict, List, Union

from faker import Faker
from sqlmodel import Session

from .db import create_db_and_tables, engine
from .models import Customer, Employee, Sales, Territory

TERRITORIES = [
    {"continent": "Africa", "country": "Rwanda"},
    {"continent": "Africa", "country": "Uganda"},
    {"continent": "Africa", "country": "Tanzania"},
    {"continent": "Africa", "country": "Burundi"},
    {"continent": "Europe", "country": "France"},
    {"continent": "Europe", "country": "Germany"},
    {"continent": "Europe", "country": "Spain"},
    {"continent": "Europe", "country": "Poland"},
    {"continent": "Asia", "country": "Singapore"},
    {"continent": "Asia", "country": "China"},
    {"continent": "Asia", "country": "Indonesia"},
    {"continent": "Asia", "country": "Vietnam"},
]


fake = Faker()
Faker.seed(0)
seed(0)


def make_random_multiplier():
    return 1 - (randint(0, 1) * 2 - 1) * random() * 0.5


def fake_ordered_dates(n, start, end):
    return sorted([fake.date_time_between_dates(start, end) for i in range(n)])


def fake_territories(
    territories: List[Dict[str, str]] = TERRITORIES,
    start: datetime = datetime(2015, 1, 1),
    end: datetime = datetime(2019, 1, 1),
) -> List[Dict[str, Union[str, datetime]]]:

    territory_dates = fake_ordered_dates(
        len(territories),
        start,
        end,
    )

    territories_with_dates = [
        {
            "continent": territory["continent"],
            "country": territory["country"],
            "created_at": date,
        }
        for date, territory in zip(territory_dates, territories)
    ]

    return territories_with_dates


def fake_data(present_date: datetime = datetime(2021, 11, 1)):

    create_db_and_tables()

    sales_year_multipliers = {
        year: make_random_multiplier()
        for year in range(present_date.year, present_date.year - 11, -1)
    }
    sales_continent_multipliers = {
        continent: make_random_multiplier()
        for continent in {"Africa", "Europe", "Asia"}
    }

    with Session(engine) as session:
        territories = fake_territories(
            territories=TERRITORIES,
            start=present_date - timedelta(days=10 * 365),  # First territory aqcisition
            end=present_date - timedelta(days=5 * 365),  # Last territory aqcisition
        )
        for territory in territories:
            t = Territory(**territory)
            min_sales_territory = fake.pyint(min_value=5, max_value=30)
            max_sales_territory = fake.pyint(min_value=100, max_value=150)
            for employee_creation_date in fake_ordered_dates(
                fake.pyint(2, 5),
                t.created_at,
                present_date - timedelta(days=4 * 365),
            ):
                e = Employee(
                    name=fake.name(),
                    created_at=employee_creation_date,
                    territory=t,
                )
                # Aquires customer once every 60 days
                min_costumers = int((present_date - e.created_at).days / 60)
                # Aquires customer once every 30 days
                max_costumers = int((present_date - e.created_at).days / 30)
                min_sales_costumers = fake.pyint(
                    min_value=min_sales_territory, max_value=min_sales_territory * 2
                )
                max_sales_costumers = fake.pyint(
                    min_value=max_sales_territory, max_value=max_sales_territory * 2
                )
                for customer_creation_date in fake_ordered_dates(
                    fake.pyint(min_costumers, max_costumers),
                    e.created_at,
                    present_date,
                ):
                    c = Customer(
                        name=fake.name(),
                        created_at=customer_creation_date,
                        territory=t,
                    )
                    # Buys once every 10 days
                    min_sales = int((present_date - e.created_at).days / 10)
                    # Buys once every 6 days
                    max_sales = int((present_date - e.created_at).days / 6)
                    min_sales_amount = fake.pyint(
                        min_value=min_sales_costumers, max_value=min_sales_costumers * 2
                    )
                    max_sales_amount = fake.pyint(
                        min_value=max_sales_costumers, max_value=max_sales_costumers * 2
                    )
                    for sales_creation_date in fake_ordered_dates(
                        fake.pyint(min_sales, max_sales),
                        c.created_at,
                        present_date,
                    ):
                        s = Sales(
                            customer=c,
                            seller=e,
                            date=sales_creation_date,
                            amount=fake.pyint(
                                min_value=min_sales_amount, max_value=max_sales_amount
                            )
                            * 100
                            * sales_year_multipliers[sales_creation_date.year]
                            * sales_continent_multipliers[t.continent],
                        )

            session.add(t)
        session.commit()


def main(present_date: datetime = datetime(2021, 11, 1)):
    create_db_and_tables()
    fake_data(present_date)


if __name__ == "__main__":
    main()
