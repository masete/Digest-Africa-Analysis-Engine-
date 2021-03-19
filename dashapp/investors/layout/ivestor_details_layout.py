import plotly.graph_objects as go
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def layout(app):
    from app import db
    from app.models import Investors

    with app.server.app_context():
        inv = db.session.query(Investors)
        data = pd.read_sql(inv.statement, inv.session.bind)

    dc = [i.lower() for i in list(data.columns)]
    data.columns = dc
    data["employees"] = data["employees"].apply(lambda x: x if len(x) > 1 else str(x).replace('-', 'Not given'))

    import plotly.express as px

    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')

    employeesdf = data[["employees", "investor"]].groupby(["employees"]).count().reset_index().sort_values(by="investor")
    employees = px.bar(employeesdf, y='employees', x='investor', orientation='h')
    employees.update_layout(
        title="Investors by number of employees",
        xaxis_title='Investors',
        yaxis_title='Number of employees'
    )

    employeesdf = data[["number_of_offices", "investor"]].groupby(["number_of_offices"]).count().reset_index().sort_values(
        by="investor")
    offices = px.pie(employeesdf, values='investor', names='number_of_offices', title='Investors by number of offices',
                     hole=.5)

    investortypeobj = {}
    data["investor_type_altered"] = data["investor_type"].apply(lambda x: str(x).replace('/', ',')
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

    for types in data["investor_type_altered"].values:
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

    agedf = data[["age", "investor"]].groupby(["age"]).count().reset_index().sort_values(by="age")
    agedf = agedf[agedf.age <= 150]
    age = px.line(agedf, x='age', y='investor')

    investorclassdf = data[["investor_class", "investor"]].groupby(["investor_class"]).count().reset_index().sort_values(
        by="investor")
    investment_class = px.pie(investorclassdf, values='investor', names='investor_class', title='Class of investors',
                              hole=.5)
    # change to app.layout if running as single page app instead
    layout = html.Div([
        dbc.Container([
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
                dbc.Col(
                    dcc.Graph(figure=age))
            ])

        ])])
    return layout
