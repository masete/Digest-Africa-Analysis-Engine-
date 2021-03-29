import dash
import pandas as pd


def register_callbacks(app):
    from app import db
    from app.models import Transactions

    with app.server.app_context():
        transact = db.session.query(Transactions)
        data = pd.read_sql(transact.statement, transact.session.bind)

    @app.callback(
        dash.dependencies.Output('output-container-range-slider', 'children'),
        [dash.dependencies.Input('year-selector', 'value')])
    def update_output(value):
        # return 'You have selected "{}"'.format(value)

        dff = data[(data["post_date"] == value)]
        

