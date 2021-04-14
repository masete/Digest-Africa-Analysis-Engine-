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

        dt_columns = data.columns

    layout = html.Div([
        dbc.Container([

            dbc.Row([
                dbc.Col(html.H6(children='Visualising data about our companies'), className="mb-4")
            ]),
            dbc.Row([
                dash_table.DataTable(
                    id='datatable-birst-category',
                    columns=[{"name": i, "id": i, 'deletable': True} for i in dt_columns],
                    editable=True,
                    fixed_columns=2,
                    style_table={'maxWidth': '1500px'},
                    row_selectable="multi",
                    selected_rows=[0],
                    style_cell={"fontFamily": "Arial", "size": 10, 'textAlign': 'left'},
                    css=[{'selector': '.dash-cell div.dash-cell-value', 'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'}],
                    style_cell_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#D5DBDB'}]
                          # + [{'if': {'column_id': c}, 'backgroundColor': '#EAFAF1'} for c in ['Spend TY', 'Spend - LP', 'Spend PoP (Abs)', 'Spend PoP (%)', 'Spend LY', 'Spend YoY (%)',]]
                          # + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#D5F5E3'} for c in ['Spend TY', 'Spend - LP', 'Spend PoP (Abs)', 'Spend PoP (%)', 'Spend LY', 'Spend YoY (%)',]]
                          # + [{'if': {'column_id': c}, 'backgroundColor': '#FEF9E7'} for c in ['Sessions - TY', 'Sessions - LP', 'Sessions - LY', 'Sessions PoP (%)', 'Sessions YoY (%)',]]
                          # + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#FCF3CF'} for c in ['Sessions - TY', 'Sessions - LP', 'Sessions - LY', 'Sessions PoP (%)', 'Sessions YoY (%)',]]
                          # + [{'if': {'column_id': c}, 'backgroundColor': '#EBF5FB'} for c in ['Bookings - TY', 'Bookings - LP', 'Bookings PoP (%)', 'Bookings PoP (Abs)', 'Bookings - LY', 'Bookings YoY (%)', 'Bookings YoY (Abs)',]]
                          # + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#D6EAF8'} for c in ['Bookings - TY', 'Bookings - LP', 'Bookings PoP (%)', 'Bookings PoP (Abs)', 'Bookings - LY', 'Bookings YoY (%)', 'Bookings YoY (Abs)',]]
                          # + [{'if': {'column_id': c},'backgroundColor': '#F4ECF7'} for c in ['CVR - TY', 'CVR - LP', 'CVR PoP (Abs)','CVR - LY',  'CVR YoY (Abs)', 'CVR PoP (%)', 'CVR YoY (%)']]
                          # + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#E8DAEF' } for c in ['CVR - TY', 'CVR - LP', 'CVR PoP (Abs)','CVR - LY',  'CVR YoY (Abs)', 'CVR PoP (%)', 'CVR YoY (%)']]
                          # + [{'if': {'column_id': c}, 'backgroundColor': '#FDEDEC' } for c in ['CPA - TY', 'CPA - LP', 'CPA PoP (Abs)', 'CPA - LY', 'CPA YoY (Abs)','CPA PoP (%)', 'CPA YoY (%)' ]]
                          # + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#FADBD8' } for c in ['CPA - TY', 'CPA - LP', 'CPA PoP (Abs)', 'CPA - LY', 'CPA YoY (Abs)', 'CPA PoP (%)', 'CPA YoY (%)']]
                          # + [{'if': {'column_id': c},'backgroundColor': '#F6DDCC'} for c in ['CPS - TY', 'CPS - LP', 'CPS PoP (Abs)', 'CPS - LY',  'CPS YoY (Abs)', 'CPS PoP (%)', 'CPA YoY (%)']]
                          # + [{'if': {'column_id': c, 'row_index': 'odd'}, 'backgroundColor': '#E59866' } for c in ['CPS - TY', 'CPS - LP', 'CPS PoP (Abs)', 'CPS - LY',  'CPS YoY (Abs)', 'CPS PoP (%)', 'CPA YoY (%)']]
                          # + [{'if': {'column_id': c}, 'minWidth': '0px', 'maxWidth': '80px', 'whiteSpace': 'normal'} for c in ['Spend TY', 'Spend - LP', 'Spend PoP (Abs)', 'Spend PoP (%)', 'Spend LY', 'Spend YoY (%)', 'Sessions - TY', 'Sessions - LP', 'Sessions - LY', 'Sessions PoP (%)',
                          # 'Sessions YoY (%)', 'Bookings - TY', 'Bookings - LP', 'Bookings PoP (%)', 'Bookings PoP (Abs)', 'Bookings - LY', 'Bookings YoY (%)', 'Bookings YoY (Abs)', 'Revenue - TY', 'Revenue - LP', 'Revenue PoP (Abs)', 'Revenue PoP (%)', 'Revenue - LY', 'Revenue YoY (%)', 'Revenue YoY (Abs)',]]
                    ),
                ], className=" twelve columns"),
        ])
    ])

    return layout
