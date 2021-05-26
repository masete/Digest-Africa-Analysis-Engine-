import pandas as pd
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from datetime import date, timedelta
import dash_bootstrap_components as dbc


def layout(app):
    from app import db
    from app.models import Transactions

    with app.server.app_context():
        transact = db.session.query(Transactions)
        data = pd.read_sql(transact.statement, transact.session.bind)
        df = data

        dt_columns = df.columns

        df['post_date'] = pd.to_datetime(df['post_date'])

        df['post_date'] = pd.to_datetime(df['post_date'], format='%Y%m%d')
        # dff = pd.DatetimeIndex(df['post_date']).year

        # current_year = dff['Year'].max()

        conditional_columns = ['country', 'main_sector', 'investors', 'link']

        df.set_index('id', inplace=True, drop=False)

    layout = html.Div([
        # Header(),
        # Date Picker
        # html.Div([
        #     dcc.DatePickerRange(
        #         id='my-date-picker-range-birst-category',
        #         # with_portal=True,
        #         min_date_allowed=dt(2018, 1, 1),
        #         max_date_allowed=df['post_date'].max().to_pydatetime(),
        #         initial_visible_month=dt(current_year, df['Date'].max().to_pydatetime().month, 1),
        #         start_date=(df['Date'].max() - timedelta(6)).to_pydatetime(),
        #         end_date=df['Date'].max().to_pydatetime(),
        #     ),
        #     html.Div(id='output-container-date-picker-range-birst-category')
        # ], className="row ", style={'marginTop': 30, 'marginBottom': 15}),
        # Header Bar
        html.Div([
            html.H6(["Company Data"], className="gs-header gs-text-header padded", style={'marginTop': 15})
        ]),
        # Radio Button
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Condensed Data Table', 'value': 'Condensed'},
                    {'label': 'Complete Data Table', 'value': 'Complete'},
                ], value='Condensed',
                labelStyle={'display': 'inline-block', 'width': '20%', 'margin': 'auto', 'marginTop': 15,
                            'paddingLeft': 15},
                id='radio-button-birst-category'
            )]),
        # First Data Table
        html.Div([
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

    return layout
