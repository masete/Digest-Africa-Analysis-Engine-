import pandas as pd
import plotly.express as px
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import dash_bootstrap_components as dbc


def layout(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entreprenuer = db.session.query(Entreprenuers)
        data = pd.read_sql(entreprenuer.statement, entreprenuer.session.bind)

        dc = [i.lower() for i in list(data.columns)]
        data.columns = dc

    # dataTables
    # dff = data[['company_name', 'amount', 'main_sector', 'company_age', 'number_of_employees', 'female_co_founder']]
    # fig_dt = go.Figure(data=[go.Table(
    #     header=dict(values=list(dff.columns),
    #                 line_color='darkslategray',
    #                 # fill_color='paleturquoise',
    #                 # align='left'
    #                 align=['left', 'center'],
    #                 font=dict(color='black', size=12),
    #                 height=40
    # ),
    #     cells=dict(values=[dff.company_name, dff.amount, dff.main_sector, dff.company_age, dff.number_of_employees,
    #                        dff.female_co_founder],
    #                line_color='darkslategray',
    #                fill=dict(color=['paleturquoise', 'white']),
    #                align=['left', 'center'],
    #                font_size=12,
    #                height=50))
    # ])

    dfff = data[['company_name', 'amount', 'main_sector', 'company_age', 'number_of_employees', 'number_of_investors']]
    dfff.rename(columns={'company_name': 'CompanyName', 'amount': 'Amount', 'main_sector': 'Main Sector',
                         'company_age' : 'Company Age', 'number_of_employees': 'Number Of Employees',
                         'number_of_investors': 'Number of Investors'}, inplace=True)

    # unique companies
    uniqueCompanies = len(data["company_name"].apply(lambda x: x.lower()).unique())

    # country headquarters
    uniqueCountries = len(data["country_hq"].apply(lambda x: x.lower()).unique())

    # main company sectors
    uniqueSectors = len(data["main_sector"].apply(lambda x: x.lower()).unique())

    Max_prev_funding = max(data["last_funding_round_raised_amount"])

    companies_df = data[["last_funding_round_raised_amount", "company_age"]].groupby(["company_age"]).count().reset_index()
    companies = px.bar(companies_df, y='company_age', x='last_funding_round_raised_amount', orientation='h')
    companies.update_layout(
        title="last funding round raised amount by company age",
        xaxis_title='last funding round raised amount',
        yaxis_title='company age'
    )

    # companies_line_plot = px.line(data, x="amount", y="company_name", title='Company name by amount')

    data.loc[(data['amount'].astype(float)) < 20.e6, 'company_name'] = 'Other companies'
    Companys_Pie_chart = px.pie(data, values='amount', names='company_name', title='amount by company name')

    layout = html.Div([
        dbc.Container([

            dbc.Row([
                dbc.Col(html.H6(children='Visualising data about our companies'), className="mb-4")
            ]),

            dbc.Row([
                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("All Companies", className="card-title"),
                            html.H4(uniqueCompanies, className="card-title"),
                        ]
                    ),
                    className="w-80",
                    color="dark",
                    inverse=True
                )]),

                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [html.H6("Countries", className="card-title"),
                         html.H4(uniqueCountries, className="card-title"),

                         ]
                    ),

                    className="w-80",
                    color="dark",
                    inverse=True
                )]),
                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Company Sectors", className="card-title"),
                            html.H4(uniqueSectors, className="card-title"),
                        ]
                    ),

                    className="w-80",
                    color="dark",
                    inverse=True
                )]),
                dbc.Col([dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Highest Amt in prev funding", className="card-title"),
                            html.H4(Max_prev_funding, className="card-title"),
                        ]
                    ),

                    className="w-80",
                    color="dark",
                    inverse=True
                )])

            ]),
            dbc.Row([
                dbc.Col([
                    html.H6(children='Startup Companies data'),
                        dcc.Dropdown(id='dropdown', options=[
                            {'label': i, 'value': i} for i in dfff.CompanyName.unique()
                        ], multi=True, placeholder='Filter by companies...'),
                        html.Div(id='table-container')
                ])
            ]),

            # dbc.Row([
            #     dbc.Col([
            #         html.H6("Our data showing some of companies, the age of the companies,"
            #                 " those founded by ladies and ammount"),
            #         dcc.Graph(figure=fig_dt)
            #     ])
            # ]),
            # dbc.Row([
            #     dbc.Col([
            #         html.H6("Our data showing some of companies, the age of the companies "
            #                 "those founded by ladies and ammount"),
            #         html.Div([
            #             dash_table.DataTable(
            #                 id='datatable-interactivity',
            #                 columns=[
            #                     {"name": i, "id": i, "deletable": True, "selectable": True} for i in data.columns],
            #                 data=data.to_dict('records'),
            #                 editable=True,
            #                 # filter_action="native",
            #                 # sort_action="native",
            #                 sort_mode="multi",
            #                 # column_selectable="single",
            #                 row_selectable="multi",
            #                 row_deletable=True,
            #                 selected_columns=[],
            #                 selected_rows=[],
            #                 # page_action="native",
            #                 page_current=0,
            #                 page_size=20,),
            #             html.Div(id='datatable-interactivity-container')
            #         ])])
            # ]),
            # dbc.Row([
            #     dbc.Col(
                    # dcc.Graph(figure=companies_line_plot)
            #     )
            # ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=Companys_Pie_chart)
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(figure=companies)
                )
            ]),
        ])])
    return layout
