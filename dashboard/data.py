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
