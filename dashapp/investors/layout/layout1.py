import plotly.graph_objects as go
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def layout(app):
    from app import db
    from app.models import Investors

    with app.server.app_context():
        invest = db.session.query(Investors)
        data = pd.read_sql(invest.statement, invest.session.bind)

    dc = [i.lower() for i in list(data.columns)]
    data.columns = dc
    uniqueUnvestors = len(data['investor'].apply(lambda x: x.lower()).unique())
    # key female
    key_female_people = data["female_key_people"][data["female_key_people"] == '1.0'].count()
    # countries
    countries_count = len(
        data["headquarters"].apply(lambda x: x.lower().replace('usa', 'united states').split(',')[-1]).unique())

    # portfolio size
    psi = data[["portfolio_size", "investor"]].groupby(["portfolio_size"]).count().reset_index()
    psi.columns = ['portfolio size', 'number of investors']
    # psi
    # active investors
    active_investors = len(data["investor"][data["status"] == 'active'].apply(lambda x: x.lower()).unique())
    # stages
    stage_count = {}
    stages = list(data["investment_stage"].apply(lambda x: x.replace('/', ', ').split(', ')))
    for stage_list in stages:
        for stage in stage_list:
            if stage in stage_count.keys():
                stage_count[stage][0] += 1
            else:
                stage_count[stage] = [1]
    stages = pd.DataFrame.from_dict(stage_count).T.reset_index()
    stages.columns = ["stages", "number of investors"]
    stages = stages.sort_values(by=["number of investors"])
    figStages = go.Figure([go.Bar(x=stages["stages"], y=stages["number of investors"], orientation='v')])
    figStages.update_layout(
        title='Investors by investment stage',
        xaxis_title="Stage",
        yaxis_title="Investors",
        height=600,
        width=600
    )
    # sectors
    sector_count = {}
    for sector_list in data["sector_of_focus"].apply(lambda x: x.split(', ')):
        for sector in sector_list:
            if sector in sector_count:
                sector_count[sector][0] += 1
            else:
                sector_count[sector] = [1]
    #
    sectors = pd.DataFrame.from_dict(sector_count).T.reset_index()
    sectors.columns = ["sectors", "number of investors"]
    sectors = sectors.sort_values(by=["number of investors"])
    sectors = sectors[sectors["sectors"] != "missing"]
    figSectors = go.Figure(data=[go.Pie(labels=sectors["sectors"], values=sectors["number of investors"], hole=.3)])
    figSectors.update_layout(
        title='Investors by sector'
    )
    # # figure
    fig = go.Figure(data=go.Scatter(x=psi['portfolio size'], y=psi['number of investors']))
    fig.update_layout(
        title='Distribution of number of investors by their portfolio size.',
        xaxis_title="portfolio size",
        yaxis_title="Number of investors",
        height=600
    )

    # change to app.layout if running as single page app instead
    layout = html.Div([
        dbc.Container([

            dbc.Row([
                dbc.Col(html.H6(children='Visualising data about our investors'), className="mb-4")
            ]),

             dbc.Row([
                 dbc.Col([ dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("All investors", className="card-title"),
                                    html.H4(uniqueUnvestors, className="card-title"),
                                ]
                            ),
                            className="w-80",
                            color="dark",
                            inverse=True
                )])
               ,
                dbc.Col([dbc.Card(
                            dbc.CardBody(
                                [   html.H6("Active investors", className="card-title"),
                                    html.H4(active_investors, className="card-title"),

                                ]
                            ),

                             className="w-80",
                             color="dark",
                            inverse=True
                )])
                ,
                dbc.Col([dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Countries", className="card-title"),
                                    html.H4(countries_count, className="card-title"),
                                ]
                            ),

                             className="w-80",
                             color="dark",
                            inverse=True
                )])
                ,
                 dbc.Col([dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Female key people", className="card-title"),
                                    html.H4(key_female_people, className="card-title"),
                                ]
                            ),
                            className="w-80",
                            color="dark",
                            inverse=True
                )])

            ]),
            dbc.Row([
                dbc.Col(
                     dcc.Graph(figure=figStages)
                )
            ,
                dbc.Col(
                     dcc.Graph(figure=figSectors)
                )
            ]),
            dbc.Row([
                dbc.Col(
                     dcc.Graph(figure=fig)
                )
            ]),
            ])])

    return layout

