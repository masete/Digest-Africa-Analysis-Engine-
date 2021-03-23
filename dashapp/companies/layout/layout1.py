import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


def layout(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entre = db.session.query(Entreprenuers)
        data = pd.read_sql(entre.statement, entre.session.bind)

        dc = [i.lower() for i in list(data.columns)]
        data.columns = dc
    data = data.sort_values(by='country_hq')
    countries = ['all'] + list(data.country_hq.unique())

    # plotting the latest funding rounds done through the platforms

    amount_count = ['amount', 'count']
    funding_round = ['largest funding round', 'latest funding round']
    main_sectors = list(set(data["main_sector"].unique()))
    business_models = list(set(data["business_model"].unique()))
    # change to app.layout if running as single page app instead
    layout = html.Div([
        dbc.Row([
            dbc.Col(
                [dcc.Graph(id='chart'),
                 html.P('This chart shows the count of last funding rounds for the companies that exist in our database. For most companies in the database,\
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
                    options=[{'label': i.lower(), 'value': i.lower()} for i in ['all'] + main_sectors],
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


    def display_value_amount_count(age_range, amount_count, main_sectors, countries_selected, funding_rounds,
                                   business_models):
        df = data.fillna(0)
        # selecting funding rounds to either latest or largetst

        if funding_rounds == 'largest funding round':
            funding_round_type = 'largest_round'
            funding_round_amount = 'last_funding_round_raised_amount'
        elif funding_rounds == 'latest funding round':
            funding_round_type = "last_funding_round_raised_type"
            funding_round_amount = 'amount'

        # filtering the selected main sectors
        if len(main_sectors) > 0:
            if (len(main_sectors) == 1) & (main_sectors[0] == 'all'):
                None
            elif 'all' in main_sectors:
                None
            else:
                df = df[df.main_sector.isin(list(main_sectors))]

        else:
            None

        # filtering the selected business models
        if len(business_models) > 0:
            if (len(business_models) == 1) & (business_models[0] == 'all'):
                None
            elif 'all' in business_models:
                None
            else:
                df = df[df.business_model.isin(list(business_models))]

        else:
            None
        # filtering the selected countries
        if len(countries_selected) > 0:
            if (len(countries_selected) == 1) & (countries_selected[0] == 'All'):
                None
            elif 'All' in countries_selected:
                None
            else:
                df = df[df.country_hq.isin([i.lower() for i in list(countries_selected)])]

        else:
            None
        # filtering the selected company age range
        df = df[(df['company_age'].astype(float) >= age_range[0]) & (df['company_age'].astype(float) <= age_range[1])]

        # filtering the selected either amount funded or count of the companies
        if amount_count == 'count':
            df = df[df[funding_round_amount].astype(float) > 0]
            df = df[['company_name', funding_round_type]] \
                .groupby([funding_round_type]) \
                .count().reset_index().sort_values(by='company_name')
            df = df[df[funding_round_type] != 'missing']
            fig = go.Figure(data=[go.Bar(
                x=df[funding_round_type],
                y=df.company_name, text=df.company_name,
            )])
            fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig.update_layout(
                title='Latest funding rounds for all the companies',
                height=600
            )
        elif amount_count == 'amount':
            df[funding_round_amount] = df[funding_round_amount].astype(float)
            df = df[df[funding_round_amount] > 0]
            df = df[[funding_round_amount, funding_round_type]] \
                .groupby([funding_round_type]) \
                .sum().reset_index().sort_values(by=funding_round_amount)
            df = df[df[funding_round_type] != 'missing']
            fig = go.Figure(data=[go.Bar(
                x=df[funding_round_type],
                y=df[funding_round_amount], text=df[funding_round_amount],
            )])
            fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig.update_layout(
                title='Latest funding rounds for all the companies',
                height=600
            )
        return fig
    return layout
