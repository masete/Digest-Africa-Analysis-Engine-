import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


def layout(app):
    from app import db
    from app.models import Transactions, Entreprenuers

    with app.server.app_context():
        transact = db.session.query(Transactions)
        data = pd.read_sql(transact.statement, transact.session.bind)

        companyx = db.session.query(Transactions)
        dealsx = db.session.query(Entreprenuers)

        company = pd.read_sql(companyx.statement, companyx.session.bind)
        deals = pd.read_sql(dealsx.statement, dealsx.session.bind)

        dc = [i.lower() for i in list(company.columns)]
        company.columns = dc

        dh = [i.lower() for i in list(deals.columns)]
        deals.columns = dh

    dc = [i.lower() for i in list(data.columns)]
    data.columns = dc

    data["post_date"] = pd.to_datetime(data["post_date"], format='%Y-%m-%d')
    data = data.sort_values(by="post_date")
    data.country = data.country.apply(lambda x: str(x).title().replace('Of', 'of'))

    df = data
    fig = px.line(df, x='post_date', y="amount")
    fig.update_layout(
        title="Timeseries for deals amount."
    )

    fig2 = px.histogram(df, x="post_date", y="amount", histfunc="avg", title="Histogram on Date Axes")
    fig2.update_traces(xbins_size="M1")
    fig2.update_xaxes(showgrid=True, ticklabelmode="period", dtick="M1", tickformat="%b\n%Y")
    fig2.update_layout(bargap=0.1)

    df = data[["post_date", "amount", "funding_round"]].groupby(["post_date"]).sum().reset_index()
    df.index = df.post_date
    df = df.drop(['post_date'], axis=1)
    df = df.cumsum()
    fig3 = px.area(df, x=df.index, y="amount")
    fig3.update_layout(
        title="Timeseries for deals amount."
    )

    df = data[['funding_round', 'amount']].groupby(['funding_round']).sum().reset_index().sort_values(by="amount")
    fig4 = px.bar(df, x='funding_round', y='amount')

    df = data[['country', 'amount']].groupby(['country']).sum().reset_index().sort_values(by="amount")
    df = df.tail(20)
    fig5 = px.bar(df, y='country', x='amount', orientation='h')
    fig5.update_layout(
        height=500
    )

    df = data[['main_sector', 'amount']].groupby(['main_sector']).sum().reset_index().sort_values(by="amount")

    df = df.tail(20)

    fig6 = px.bar(df, y='main_sector', x='amount', orientation='h')
    fig6.update_layout(
        height=500
    )

    df = data[['country', 'main_sector', 'funding_round', 'amount']].groupby(
        ['country', 'main_sector', 'funding_round']).sum().reset_index()
    df.amount = df.amount.apply(lambda x: x if x > 0 else 1)
    fig7 = px.treemap(df, path=[px.Constant('Funding'), 'country', 'funding_round'], values='amount',
                      color='amount', hover_data=['amount'])
    fig7.update_layout(
        height=700
    )

    # second layout

    company_deals_merged = pd.merge(left=deals, right=company, left_on=['company_name'], right_on=['title'])
    data1 = company_deals_merged[
        ['company_name', 'business_model', 'number_of_operational_countries', 'number_of_investors_y',
         'female_co_founder',
         'attended_accelerator', 'amount_y']]

    dff = data1[['amount_y', 'attended_accelerator']].groupby(['attended_accelerator']).sum().reset_index()
    fig_pie = px.pie(dff, values='amount_y', names='attended_accelerator', hole=.5,
                 color_discrete_sequence=['#8E6C8A', '#6B99A1'])
    fig.update_layout(
        title='Amount against accelerator attendance'
    )

    dff = data1[['amount_y', 'female_co_founder']].groupby(['female_co_founder']).sum().reset_index()
    fig2_pie = px.pie(dff, values='amount_y', names='female_co_founder', hole=.5, color_discrete_sequence=['#E58429',
                                                                                                       '#E3BA22'])
    fig2_pie.update_layout(
        title='Amount against female co-founder'
    )

    dff = data1[['amount_y', 'number_of_investors_y']].groupby(['number_of_investors_y']).sum().reset_index()
    dff['number_of_investors_y'] = pd.to_numeric(dff['number_of_investors_y'])
    df = dff.sort_values(by='number_of_investors_y')
    fig3 = px.area(df, x="number_of_investors_y", y="amount_y",
                   title='Deal amount against number of investors on one deal.')

    # fig4 = go.Figure()
    # fig4.add_trace(go.Scatter(x=df.number_of_investors_y, y=df.amount_y, fill='tozeroy', line_color='#E58429',
    #                           mode='lines'
    #                           ))

    dff = data1[['amount_y', 'number_of_operational_countries']].groupby(
        ['number_of_operational_countries']).sum().reset_index()
    dff['number_of_operational_countries'] = pd.to_numeric(dff['number_of_operational_countries'])
    dff = dff.sort_values(by='number_of_operational_countries')
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=dff.number_of_operational_countries, y=dff.amount_y, fill='tozeroy', line_color='#5C8100',
                              mode='lines'
                              ))

    # change to app.layout if running as single page app instead
    layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1(children='Transactions'), className="mb-2")
            ]),
            html.Div([
                dcc.RangeSlider(
                    id='year-selector',
                    min=2000,
                    max=2021,
                    dots=True,
                    # step=0.5,
                    value=[2018],
                    marks={int(yr): str(yr) for yr in range(2000, 2021, 4)}

                ),
                html.Div(id='output-container-range-slider')
            ]),
            dbc.Row([
                dbc.Col(html.H6(children='Deals'), className="mb-4")
            ]),

            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        options=[
                            {'label': i, 'value': i} for i in deals.company_name.unique()
                        ],
                        # options=[
                        #     {'label': 'New York City', 'value': 'NYC'},
                        #     {'label': 'Montreal', 'value': 'MTL'},
                        #     {'label': 'San Francisco', 'value': 'SF'}
                        # ],
                        # value=['MTL', 'NYC'],
                        multi=True
                    )

                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig)

                )

            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig2)

                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig3)

                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig4)

                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig5)

                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig6)

                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=fig7)

                )
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig_pie)
                ]),
                dbc.Col([
                    dcc.Graph(figure=fig2_pie)
                ])

            ]),

        ])])
    return layout
