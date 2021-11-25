import os

import pandas as pd
import requests

API_URL = os.environ.get("API_URL")


def get_top10_employees(continent):
    response = requests.get(API_URL + f"topn_employees/{continent}/10")
    df = pd.DataFrame(response.json())
    df = df.assign(
        total_sales=df.total_sales.round(2),
        average_sale_amount=df.average_sale_amount.round(2),
    )
    return df


def get_top100_customers(continent):
    response = requests.get(API_URL + f"top100_customers/{continent}")
    df = pd.DataFrame(response.json())
    df = df.assign(
        total_purchases=df.total_purchases.round(2),
        average_purchase_amount=df.average_purchase_amount.round(2),
        days_as_customer=(
            (
                (
                    pd.to_datetime(df.last_purchase) - pd.to_datetime(df.first_purchase)
                ).dt.total_seconds()
            )
            / (3600 * 24)
        )
        .round(0)
        .map(int),
    )
    df = df.assign(
        avg_days_between_purchases=(df.days_as_customer / df.number_of_purchases).round(
            1
        ),
    )
    return df
