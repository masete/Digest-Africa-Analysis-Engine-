import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px


def layout(app):
    from app import db
    from app.models import Transactions

    with app.server.app_context():
        transact = db.session.query(Transactions)
        data = pd.read_sql(transact.statement, transact.session.bind)

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

    # change to app.layout if running as single page app instead
    layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1(children='Transactions'), className="mb-2")
            ]),
            dbc.Row([
                dbc.Col(html.H6(children='Deals'), className="mb-4")
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
            ])

        ])])
    return layout
