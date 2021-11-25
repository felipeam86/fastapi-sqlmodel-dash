import plotly.express as px


def total_sales_year_graph(df_sales_year):
    return px.bar(df_sales_year.reset_index(), x="year", y="total_sales")


def average_sale_year_graph(df_sales_year):
    return px.bar(df_sales_year.reset_index(), x="year", y="average_sale_amount")


def total_sales_year_per_country_graph(df_sales):
    return px.bar(
        df_sales.reset_index(),
        x="year",
        y="total_sales",
        color="country",
        facet_col="continent",
        barmode="relative",
    )
