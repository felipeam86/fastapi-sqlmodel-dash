from datetime import datetime
from typing import Dict, List, Union

from faker import Faker


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
