import pandas as pd
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def layout(app):
    from app import db
    from app.models import Transactions

    with app.server.app_context():
        transact = db.session.query(Transactions)
        data = pd.read_sql(transact.statement, transact.session.bind)
        df = data

        dt_columns = df.columns

        conditional_columns = ['country', 'main_sector', 'investors', 'link',]

        df.set_index('id', inplace=True, drop=False)

    layout = html.Div([
        dbc.Container([

            dbc.Row([
                dbc.Col(html.H6(children='Visualising data about our companies'), className="mb-4")
            ]),
            dbc.Row([
                dash_table.DataTable(
                    id='datatable-interactivity',
                    columns=[{"name": i, "id": i, 'deletable': True} for i in dt_columns]
                            + [{"name": j, "id": j, 'hidden': 'True'} for j in conditional_columns],
                    data=df.to_dict('records'),  # the contents of the table
                    editable=True,  # allow editing of data inside all cells
                    filter_action="native",  # allow filtering of data by user ('native') or not ('none')
                    sort_action="native",  # enables data to be sorted per-column by user or not ('none')
                    sort_mode="single",  # sort across 'multi' or 'single' columns
                    column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                    row_selectable="multi",  # allow users to select 'multi' or 'single' rows
                    row_deletable=True,  # choose if user can delete a row (True) or not (False)
                    selected_columns=[],  # ids of columns that user selects
                    selected_rows=[],  # indices of rows that user selects
                    page_action="native",  # all data is passed to the table up-front or not ('none')
                    page_current=0,  # page number that user is on
                    page_size=6,  # number of rows visible per page
                    css=[{'selector': '.dash-cell div.dash-cell-value',
                          'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                    fixed_columns=2,
                    style_table={'maxWidth': '1500px'},
                    # row_selectable="multi",
                    style_cell={"fontFamily": "Arial", "size": 10, 'textAlign': 'left'},
                    # style_cell={  # ensure adequate header width when text is shorter than cell's text
                    #     'minWidth': 95, 'maxWidth': 95, 'width': 95
                    # },
                    style_cell_conditional=[  # align text columns to left. By default they are aligned to right
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['country', 'iso_alpha3']
                    ],
                    style_data={  # overflow cells' content into multiple lines
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    }
                ),

                html.Br(),
                html.Br(),
                html.Div(id='bar-container'),
                html.Div(id='choromap-container')

            ])
        ])
    ])

    return layout
