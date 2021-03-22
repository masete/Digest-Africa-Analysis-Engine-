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
        companyx = db.session.query(Transactions)
        dealsx = db.session.query(Entreprenuers)

        company = pd.read_sql(companyx.statement, companyx.session.bind)
        deals = pd.read_sql(dealsx.statement, dealsx.session.bind)

        deals.columns

    company_deals_merged = pd.merge(left=company, right=deals, left_on='company_name', right_on='title')
    data = company_deals_merged[
        ['company_name', 'business_model', 'number_of_operational_countries', 'number_of_investors_y',
         'female_co_founder',
         'attended_accelerator', 'amount_y']]

    df = data[['amount_y', 'attended_accelerator']].groupby(['attended_accelerator']).sum().reset_index()
    fig = px.pie(df, values='amount_y', names='attended_accelerator', hole=.5,
                 color_discrete_sequence=['#8E6C8A', '#6B99A1'])
    fig.update_layout(
        title='Amount against accelerator attendance'
    )

    df = data[['amount_y', 'female_co_founder']].groupby(['female_co_founder']).sum().reset_index()
    fig2 = px.pie(df, values='amount_y', names='female_co_founder', hole=.5, color_discrete_sequence=['#E58429',
                                                                                                      '#E3BA22'])
    fig2.update_layout(
        title='Amount against female co-founder'
    )

    df = data[['amount_y', 'number_of_investors_y']].groupby(['number_of_investors_y']).sum().reset_index()
    df['number_of_investors_y'] = pd.to_numeric(df['number_of_investors_y'])
    df = df.sort_values(by='number_of_investors_y')
    fig3 = px.area(df, x="number_of_investors_y", y="amount_y",
                   title='Deal amount against number of investors on one deal.')

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df.number_of_investors_y, y=df.amount_y, fill='tozeroy', line_color='#E58429',
                              mode='lines'
                              ))

    df = data[['amount_y', 'number_of_operational_countries']].groupby(
        ['number_of_operational_countries']).sum().reset_index()
    df['number_of_operational_countries'] = pd.to_numeric(df['number_of_operational_countries'])
    df = df.sort_values(by='number_of_operational_countries')
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=df.number_of_operational_countries, y=df.amount_y, fill='tozeroy', line_color='#5C8100',
                              mode='lines'
                              ))

    df = data[['business_model', 'amount_y']].groupby(['business_model']).sum().reset_index()
    df = df.sort_values(by='amount_y')
    x = df.business_model
    y = df.amount_y
    # Use the hovertext kw argument for hover text
    fig6 = go.Figure(data=[go.Bar(x=x, y=y,
                                  hovertext=['27% market share', '24% market share', '19% market share'])])
    # Customize aspect
    fig6.update_traces(marker_color='#E58429', marker_line_color='#BD2D28',
                       marker_line_width=1.5, opacity=0.6)
    fig6.update_layout(title_text='January 2013 Sales Report')
    print(df)
    layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig)
                ]),
                dbc.Col([
                    dcc.Graph(figure=fig2)
                ])

            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig4)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=fig6)
                ])
            ])
        ])
    ])
    return layout
