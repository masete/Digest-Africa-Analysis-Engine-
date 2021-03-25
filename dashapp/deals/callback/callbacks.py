from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table
import dash
from flask_login import current_user
import pandas as pd
from collections import OrderedDict
from sqlalchemy.exc import IntegrityError
import dashapp.deals.layout


def register_callbacks(app):
    from app import db
    from app.models import Transactions

    @app.callback(
        dash.dependencies.Output('output-container-range-slider', 'children'),
        [dash.dependencies.Input('year-selector', 'value')])
    def update_output(value):
        return 'You have selected "{}"'.format(value)
