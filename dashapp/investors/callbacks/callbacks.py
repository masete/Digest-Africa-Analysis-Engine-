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



    # filtering age of the company
