import pandas as pd
import dash_table
import dash_html_components as html


def layout(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entre = db.session.query(Entreprenuers)
        data = pd.read_sql(entre.statement, entre.session.bind)

        dc = [i.lower() for i in list(data.columns)]
        data.columns = dc

    layout = html.Div(
        className="row",
        children=[
            html.Div(
                dash_table.DataTable(
                    id='table-paging-with-graph',
                    columns=[
                        {"name": i, "id": i} for i in sorted(data.columns)
                    ],
                    page_current=0,
                    page_size=20,
                    page_action='custom',

                    filter_action='custom',
                    filter_query='',

                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[]
                ),
                style={'height': 750, 'overflowY': 'scroll'},
                className='six columns'
            ),
            html.Div(
                id='table-paging-with-graph-container',
                className="ten columns"
            )
        ]
    )
    return layout
