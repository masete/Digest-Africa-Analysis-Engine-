import pandas as pd
import plotly.express as px

import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc


def layout(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entreprenuer = db.session.query(Entreprenuers)
        data = pd.read_sql(entreprenuer.statement, entreprenuer.session.bind)

        dc = [i.lower() for i in list(data.columns)]
        data.columns = dc

    # unique companies
    uniqueCompanies = len(data["company_name"].apply(lambda x: x.lower()).unique())

    # country headquarters
    uniqueCountries = len(data["country_hq"].apply(lambda x: x.lower()).unique())

    # main company sectors
    uniqueSectors = len(data["main_sector"].apply(lambda x: x.lower()).unique())

    Max_prev_funding = max(data["last_funding_round_raised_amount"])

    companies_df = data[["last_funding_round_raised_amount", "company_age"]].groupby(["company_age"]).count().reset_index()
    companies = px.bar(companies_df, y='company_age', x='last_funding_round_raised_amount', orientation='h')
    companies.update_layout(
        title="last funding round raised amount by company age",
        xaxis_title='last funding round raised amount',
        yaxis_title='company age'
    )

    # companies_line_plot = px.line(data, x="amount", y="company_name", title='Company name by amount')

    data.loc[(data['amount'].astype(float)) < 20.e6, 'company_name'] = 'Other companies'
    Companys_Pie_chart = px.pie(data, values='amount', names='company_name', title='amount by company name')

    layout = html.Div([
        dbc.Container([

            dbc.Row([
                dbc.Col(html.H6(children='Visualising data about our companies'), className="mb-4")
            ]),

            dbc.Row([
                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("All Companies", className="card-title"),
                            html.H4(uniqueCompanies, className="card-title"),
                        ]
                    ),
                    className="w-80",
                    color="dark",
                    inverse=True
                )]),

                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [html.H6("Countries", className="card-title"),
                         html.H4(uniqueCountries, className="card-title"),

                         ]
                    ),

                    className="w-80",
                    color="dark",
                    inverse=True
                )]),
                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Company Sectors", className="card-title"),
                            html.H4(uniqueSectors, className="card-title"),
                        ]
                    ),

                    className="w-80",
                    color="dark",
                    inverse=True
                )]),
                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Highest Amt in prev funding", className="card-title"),
                            html.H4(Max_prev_funding, className="card-title"),
                        ]
                    ),

                    className="w-80",
                    color="dark",
                    inverse=True
                )])

            ]),

            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=companies)
                )
            ]),
            dbc.Row([
                dbc.Col(
                    # dcc.Graph(figure=companies_line_plot)
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=Companys_Pie_chart)
                )
            ]),
        ])])
    return layout
