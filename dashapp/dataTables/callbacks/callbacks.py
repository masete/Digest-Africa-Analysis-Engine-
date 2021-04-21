from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly import tools

from datetime import datetime as dt
from datetime import date, timedelta
from datetime import datetime

import numpy as np
import pandas as pd


def register_callbacks(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entre = db.session.query(Entreprenuers)
        df = pd.read_sql(entre.statement, entre.session.bind)

        dc = [i.lower() for i in list(df.columns)]
        df.columns = dc

    def make_dash_table(df):
        '''
        Return a dash definition of an HTML table for a Pandas dataframe
        '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    # Callback and update first data table
    # @app.callback(Output('datatable-birst-category', 'data'),
    #               [Input('my-date-picker-range-birst-category', 'start_date'),
    #                Input('my-date-picker-range-birst-category', 'end_date')])
    # def update_data_1(start_date, end_date):
    #     data_1 = update_first_datatable(start_date, end_date, None, 'Birst Category')
    #     return data_1

    # Callback and update data table columns
    # @app.callback(Output('datatable-birst-category', 'columns'),
    #               [Input('radio-button-birst-category', 'value')])
    # def update_columns(value):
    #     if value == 'Complete':
    #         column_set = [{"name": i, "id": i, "deletable": True} for i in columns_complete]
    #     elif value == 'Condensed':
    #         column_set = [{"name": i, "id": i, "deletable": True} for i in columns_condensed]
    #     return column_set
