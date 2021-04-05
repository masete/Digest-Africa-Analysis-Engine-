import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def layout(app):
    from app import db
    from app.models import Investors, Entreprenuers

    with app.server.app_context():
        invest = db.session.query(Investors)
        data1 = pd.read_sql(invest.statement, invest.session.bind)

        entreprenuer = db.session.query(Entreprenuers)
        data = pd.read_sql(entreprenuer.statement, entreprenuer.session.bind)

    dc = [i.lower() for i in list(data1.columns)]
    data1.columns = dc
    uniqueUnvestors = len(data1['investor'].apply(lambda x: x.lower()).unique())
    # key female
    key_female_people = data1["female_key_people"][data1["female_key_people"] == '1.0'].count()
    # countries
    countries_count = len(
        data1["headquarters"].apply(lambda x: x.lower().replace('usa', 'united states').split(',')[-1]).unique())

    # portfolio size
    psi = data1[["portfolio_size", "investor"]].groupby(["portfolio_size"]).count().reset_index()
    psi.columns = ['portfolio size', 'number of investors']
    # psi
    # active investors
    active_investors = len(data1["investor"][data1["status"] == 'active'].apply(lambda x: x.lower()).unique())
    # stages
    stage_count = {}
    stages = list(data1["investment_stage"].apply(lambda x: x.replace('/', ', ').split(', ')))
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
    for sector_list in data1["sector_of_focus"].apply(lambda x: x.split(', ')):
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
    fig_bar = go.Figure(data=go.Scatter(x=psi['portfolio size'], y=psi['number of investors']))
    fig_bar.update_layout(
        title='Distribution of number of investors by their portfolio size.',
        xaxis_title="portfolio size",
        yaxis_title="Number of investors",
        height=600
    )

    # investor details layout
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')

    employeesdf = data1[["employees", "investor"]].groupby(["employees"]).count().reset_index().sort_values(by="investor")
    employees = px.bar(employeesdf, y='employees', x='investor', orientation='h')
    employees.update_layout(
        title="Investors by number of employees",
        xaxis_title='Investors',
        yaxis_title='Number of employees'
    )

    employeesdf = data1[["number_of_offices", "investor"]].groupby(["number_of_offices"]).count().reset_index().sort_values(
        by="investor")
    offices = px.pie(employeesdf, values='investor', names='number_of_offices', title='Investors by number of offices',
                     hole=.5)

    investortypeobj = {}
    data1["investor_type_altered"] = data1["investor_type"].apply(lambda x: str(x).replace('/', ',')
                                                                .replace('private equity firm', 'private equity')
                                                                .replace('private  equity', 'private equity')
                                                                .replace('angel(ins)', 'angel')
                                                                .replace('angel investment', 'angel')
                                                                .replace('government venture capital', 'venture capital')
                                                                .replace('corporate venture capital', 'venture capital')
                                                                .replace('venure capital', 'venture capital')
                                                                .replace('angel (ins)', 'angel')
                                                                .replace('private euity', 'private equity')
                                                                .split(', '))

    for types in data1["investor_type_altered"].values:
        for inv_type in types:
            if inv_type in investortypeobj.keys():
                investortypeobj[inv_type][0] += 1
            else:
                investortypeobj[inv_type] = [1]
    investortypeobjdf = pd.DataFrame.from_dict(investortypeobj).T.reset_index()
    investortypeobjdf.columns = ['investor_type', 'investor']
    investortypeobjdf = investortypeobjdf.sort_values(by="investor")

    investortype = px.bar(investortypeobjdf, y='investor_type', x='investor', orientation='h')
    investortype.update_layout(
        title="Type of investors",
        xaxis_title="Investors",
        yaxis_title="Type of investors"

    )

    agedf = data1[["age", "investor"]].groupby(["age"]).count().reset_index().sort_values(by="age")
    agedf = agedf[agedf.age <= 150]
    age = px.line(agedf, x='age', y='investor')

    investorclassdf = data1[["investor_class", "investor"]].groupby(["investor_class"]).count().reset_index().sort_values(
        by="investor")
    investment_class = px.pie(investorclassdf, values='investor', names='investor_class', title='Class of investors',
                              hole=.5)

    # investor map layout

    df = px.data.election()
    geojson = px.data.election_geojson()
    candidates = df.winner.unique()
    df2 = px.data.gapminder().query("year==2007")

    fig = px.choropleth(df2, locations="iso_alpha",
                        color="lifeExp",  # lifeExp is a column of gapminder
                        hover_name="country",  # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma,
                        scope='africa')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig2 = px.choropleth(df2, locations="iso_alpha",
                         color="lifeExp",  # lifeExp is a column of gapminder
                         hover_name="country",  # column to add to hover information
                         color_continuous_scale=px.colors.sequential.Plasma,
                         )
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # change to app.layout if running as single page app instead
    layout = html.Div([
        dbc.Container([

            dbc.Row([
                dbc.Col(html.H6(children='Visualising data about our investors'), className="mb-4")
            ]),

             dbc.Row([
                 dbc.Col([dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("All investors", className="card-title"),
                                    html.H4(uniqueUnvestors, className="card-title"),
                                ]
                            ),
                            className="w-80",
                            color="dark",
                            inverse=True
                    )
                 ]),
                dbc.Col([dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H6("Active investors", className="card-title"),
                                    html.H4(active_investors, className="card-title"),

                                ]
                            ),

                             className="w-80",
                             color="dark",
                            inverse=True
                )]),
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
                )]),
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
                    )
                 ])

                ]),
            dbc.Row([

                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Investors who have had exits", className="card-title"),
                            html.H4(200, className="card-title"),
                        ]
                    ),
                    className="w-80",
                    color="dark",
                    inverse=True
                )])
                ,
                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [html.H6("Impact focus investors", className="card-title"),
                         html.H4(500, className="card-title"),

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
                            html.H6("High activity in Africa", className="card-title"),
                            html.H4(3000, className="card-title"),
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
                            html.H6("Medium activity in Africa", className="card-title"),
                            html.H4(23002, className="card-title"),
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
                ),
                dbc.Col(
                     dcc.Graph(figure=figSectors)
                )
            ]),
            dbc.Row([
                dbc.Col(
                     dcc.Graph(figure=fig_bar)
                ),
                dbc.Col(
                    dcc.Graph(figure=age))
            ])
            ,
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=employees)),
                dbc.Col(
                    dcc.Graph(figure=offices))
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=investortype)),
                dbc.Col(
                    dcc.Graph(figure=investment_class))
            ]),

            dbc.Row([
                dbc.Col([
                    html.H5("Investors by their geographical focus"),
                    dcc.Graph(figure=fig)
                ])
                ,

                dbc.Col([
                    html.H5("Investors by their headquarters"),
                    dcc.Graph(figure=fig2)
                ]),
            ])
        ])
    ])

    return layout
