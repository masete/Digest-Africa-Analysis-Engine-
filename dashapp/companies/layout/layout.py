import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


def layout(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entreprenuer = db.session.query(Entreprenuers)
        data = pd.read_sql(entreprenuer.statement, entreprenuer.session.bind)

    amount_count = ['amount', 'count']
    funding_round = ['largest funding round', 'latest funding round']
    Main_sectors = list(set(data["Main_sector"].unique()))
    business_models = list(set(data["Business_Model"].unique()))
    countries = list(set(data["Country_HQ"].unique()))

    layout = html.Div([
        dbc.Row([
            dbc.Col(
                [dcc.Graph(id='chart'),
                 html.P('This chart shows the count of last funding rounds for the companies that exist in our'
                        ' database. For most companies in the database,\
                    their last funding round is {}', style={'top': 100, 'font-size': 12})]
                , width={'size': 8, 'offset': 1}, ),
            dbc.Col([
                html.Div(html.H5('Countries HQ:')),
                dcc.Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in [i.title() for i in countries]],
                    value='All',
                    multi=True
                ),
                html.Div(html.H5('Amount or count:')),

                dcc.Dropdown(
                    id='amount_count_input',
                    options=[{'label': i, 'value': i} for i in amount_count],
                    value='count',
                ),
                html.Div(html.H5('Funding rounds:')),

                dcc.Dropdown(
                    id='input_funding_round',
                    options=[{'label': i, 'value': i} for i in funding_round],
                    value='latest funding round'
                ),
                html.Div(html.H5('Main sectors:')),

                dcc.Dropdown(
                    id='main_sector_input',
                    options=[{'label': i.lower(), 'value': i.lower()} for i in ['all'] + Main_sectors],
                    value=['all'],
                    multi=True
                ),
                html.Div(html.H5('Business models:')),

                dcc.Dropdown(
                    id='business_model_input',
                    options=[{'label': i.lower(), 'value': i.lower()} for i in ['all'] + business_models],
                    value=['all'],
                    multi=True
                ),

                html.Div(html.H5('Business age range:')),
                dcc.RangeSlider(
                    id='age_range_input',
                    marks={i: '{}'.format(i) for i in range(0, 50, 5)},
                    min=0,
                    max=41,
                    value=[0, 10]),
            ], width=3, style={'top': 100, 'font-size': 12})

        ], style={'margin-right': 2})
    ])


    return layout

