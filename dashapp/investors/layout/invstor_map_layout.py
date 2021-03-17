import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

df = px.data.election()
geojson = px.data.election_geojson()
candidates = df.winner.unique()

# import plotly.express as px


def layout(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entreprenuer = db.session.query(Entreprenuers)
        data = pd.read_sql(entreprenuer.statement, entreprenuer.session.bind)
    df2 = px.data.gapminder().query("year==2007")
    # from app import app

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

    layout = html.Div([
        dbc.Container([

            dbc.Row([
                dbc.Col([
                    html.H5("Investors by their geographical focus"),
                    dcc.Graph(figure=fig)
                ])
                ,

                dbc.Col([
                    html.H5("Investors by their headquarters"),
                    dcc.Graph(figure=fig2)
                ])
            ])
        ])
    ])
    return layout
