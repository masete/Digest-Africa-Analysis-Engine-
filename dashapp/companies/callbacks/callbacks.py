from dash.dependencies import Input, Output, State
import dash
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy.exc import IntegrityError
# amount_count = ['amount', 'count']
funding_round = ['largest funding round', 'latest funding round']


def register_callbacks(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entreprenuer = db.session.query(Entreprenuers)
        data = pd.read_sql(entreprenuer.statement, entreprenuer.session.bind)

        # print(data)

    # filtering age of the company
    @app.callback(
        dash.dependencies.Output(component_id='chart', component_property='figure'),
        [
            dash.dependencies.Input(component_id='age_range_input', component_property='value'),
            dash.dependencies.Input(component_id='amount_count_input', component_property='value'),
            dash.dependencies.Input(component_id='main_sector_input', component_property='value'),
            dash.dependencies.Input('dropdown', 'value'),
            dash.dependencies.Input('input_funding_round', 'value'),
            dash.dependencies.Input('business_model_input', 'value')
        ]
    )
    def display_value_amount_count(age_range, countries_selected, funding_rounds):

        # global funding_round_amount, funding_round_type
        df = data.fillna(0)
        main_sectors = list(set(data["Main_sector"].unique()))
        business_models = list(set(data["Business_Model"].unique()))
        amount_count = ['amount', 'count']
        funding_round = ['largest funding round', 'latest funding round']
        countries = list(set(data["Country_HQ"].unique()))
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
            go.Figure(data=[go.Bar(
                x=df[funding_round_type],
                y=df[funding_round_amount], text=df[funding_round_amount],
            )])
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(
                title='Latest funding rounds for all the companies',
                height=600
            )

        return fig
        # return {
        #     "data": [
        #         go.Bar(x=df_subcat.amount * -1, y=df_subcat.index, orientation="h")
        #     ]
        # }

        # return {
        #     "data": [
        #         go.Bar(x=df[funding_round_type], y=df[funding_round_amount], text=df[funding_round_amount])]
        # }

# return app.callback(callback.outputs, callback.inputs)(callback.f)
