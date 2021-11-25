import dash
import dash_bootstrap_components as dbc
import data
import plot
from dash import Input, Output, dcc, html

app = dash.Dash(
    title="Sales Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.config.suppress_callback_exceptions = True


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sales", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Global overview", href="/global", active="exact"),
                dbc.NavLink("Regional view", href="/region", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

region = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Region overview"),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="Africa", tab_id="Africa"),
                dbc.Tab(label="Europe", tab_id="Europe"),
                dbc.Tab(label="Asia", tab_id="Asia"),
            ],
            id="tabs",
            active_tab="Africa",
        ),
        dcc.Graph(
            id="region_graph",
        ),
        html.Div(id="top_employees"),
        html.Div(id="top_customers"),
    ]
)


df_sales, df_sales_year = data.get_year_by_year_sales()

overview = dbc.Container(
    [
        html.H1("Global overview"),
        html.Hr(),
        html.H2("Sales overview"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="total_sales_year_graph",
                        figure=plot.total_sales_year_graph(df_sales_year),
                    )
                ),
                dbc.Col(
                    dcc.Graph(
                        id="average_sale_year_graph",
                        figure=plot.average_sale_year_graph(df_sales_year),
                    )
                ),
            ]
        ),
        html.Hr(),
        html.H2("Sales per continent and country"),
        dcc.Graph(
            id="total_sales_year_per_country_graph",
            figure=plot.total_sales_year_per_country_graph(df_sales),
        ),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/global":
        return overview
    elif pathname == "/region":
        return region
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        dbc.Container(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    [
        Output("region_graph", "figure"),
        Output("top_employees", "children"),
        Output("top_customers", "children"),
    ],
    [Input("tabs", "active_tab")],
)
def render_continent_tab_content(continent_tab):
    if continent_tab is not None:
        df_employees = data.get_top10_employees(continent_tab)
        table_employees = dbc.Table.from_dataframe(
            df_employees,
            striped=True,
            bordered=True,
            hover=True,
        )
        df_customers = data.get_top100_customers(continent_tab)
        table_customers = dbc.Table.from_dataframe(
            df_customers,
            striped=True,
            bordered=True,
            hover=True,
        )
        return {}, table_employees, table_customers


if __name__ == "__main__":
    app.run_server(port=8050, host="0.0.0.0", debug=True)
