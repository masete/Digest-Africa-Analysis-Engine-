from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd


def register_callbacks(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entre = db.session.query(Entreprenuers)
        df = pd.read_sql(entre.statement, entre.session.bind)

        dc = [i.lower() for i in list(df.columns)]
        df.columns = dc

        @app.callback(
            Output('datatable-interactivity', 'style_data_conditional'),
            Input('datatable-interactivity', 'selected_columns')
        )
        def update_styles(selected_columns):
            return [{
                'if': {'column_id': i},
                'background_color': '#D2F3FF'
            } for i in selected_columns]

        @app.callback(
            Output('datatable-interactivity-container', "children"),
            Input('datatable-interactivity', "derived_virtual_data"),
            Input('datatable-interactivity', "derived_virtual_selected_rows"))
        def update_graphs(rows, derived_virtual_selected_rows):
            # When the table is first rendered, `derived_virtual_data` and
            # `derived_virtual_selected_rows` will be `None`. This is due to an
            # idiosyncrasy in Dash (unsupplied properties are always None and Dash
            # calls the dependent callbacks when the component is first rendered).
            # So, if `rows` is `None`, then the component was just rendered
            # and its value will be the same as the component's dataframe.
            # Instead of setting `None` in here, you could also set
            # `derived_virtual_data=df.to_rows('dict')` when you initialize
            # the component.
            if derived_virtual_selected_rows is None:
                derived_virtual_selected_rows = []

            dff = df if rows is None else pd.DataFrame(rows)

            colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
                      for i in range(len(dff))]

            return [
                dcc.Graph(
                    id=column,
                    figure={
                        "data": [
                            {
                                "x": dff["company_name"],
                                "y": dff[column],
                                "type": "bar",
                                "marker": {"color": colors},
                            }
                        ],
                        "layout": {
                            "xaxis": {"automargin": True},
                            "yaxis": {
                                "automargin": True,
                                "title": {"text": column}
                            },
                            "height": 250,
                            "margin": {"t": 10, "l": 10, "r": 10},
                        },
                    },
                )
                # check if column exists - user may have deleted it
                # If `column.deletable=False`, then you don't
                # need to do this check.
                for column in ["amount", "company_age", "Largest_round"] if column in dff
            ]

