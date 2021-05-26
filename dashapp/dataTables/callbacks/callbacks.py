import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd


def register_callbacks(app):
    from app import db
    from app.models import Entreprenuers

    with app.server.app_context():
        entre = db.session.query(Entreprenuers)
        df = pd.read_sql(entre.statement, entre.session.bind)

        dc = [i.lower() for i in list(df.columns)]
        df.columns = dc

        # df['id'] = df['iso_alpha3']
        df.set_index('id', inplace=True, drop=False)

    @app.callback(
        Output(component_id='bar-container', component_property='children'),
        [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
         Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
         Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
         Input(component_id='datatable-interactivity', component_property='selected_rows'),
         Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
         Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
         Input(component_id='datatable-interactivity', component_property='active_cell'),
         Input(component_id='datatable-interactivity', component_property='selected_cells')]
    )
    def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
                   order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
        print('***************************************************************************')
        print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
        print('---------------------------------------------')
        print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
        print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
        print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
        print('---------------------------------------------')
        print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
        print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
        print("---------------------------------------------")
        print("Complete data of active cell: {}".format(actv_cell))
        print("Complete data of all selected cells: {}".format(slctd_cell))

        dff = pd.DataFrame(all_rows_data)

        # used to highlight selected countries on bar chart
        colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
                  for i in range(len(dff))]

        if "country" in dff and "did online course" in dff:
            return [
                dcc.Graph(id='bar-chart',
                          figure=px.bar(
                              data_frame=dff,
                              x="country",
                              y='did online course',
                              labels={"did online course": "% of Pop took online course"}
                          ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                          .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
                          )
            ]

    # -------------------------------------------------------------------------------------
    # Create choropleth map
    # @app.callback(
    #     Output(component_id='choromap-container', component_property='children'),
    #     [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
    #      Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows')]
    # )
    # def update_map(all_rows_data, slctd_row_indices):
    #     dff = pd.DataFrame(all_rows_data)
    #
    #     # highlight selected countries on map
    #     borders = [5 if i in slctd_row_indices else 1
    #                for i in range(len(dff))]
    #
    #     if "iso_alpha3" in dff and "internet daily" in dff and "country" in dff:
    #         return [
    #             dcc.Graph(id='choropleth',
    #                       style={'height': 700},
    #                       figure=px.choropleth(
    #                           data_frame=dff,
    #                           locations="iso_alpha3",
    #                           scope="africa",
    #                           color="internet daily",
    #                           title="% of Pop that Uses Internet Daily",
    #                           template='plotly_dark',
    #                           hover_data=['country', 'internet daily'],
    #                       ).update_layout(showlegend=False, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
    #                       .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
    #                                                                               "%{customdata[1]}" + "%")
    #                       )
    #         ]

    # -------------------------------------------------------------------------------------
    # Highlight selected column
    @app.callback(
        Output('datatable-interactivity', 'style_data_conditional'),
        [Input('datatable-interactivity', 'selected_columns')]
    )
    def update_styles(selected_columns):
        return [{
            'if': {'column_id': i},
            'background_color': '#D2F3FF'
        } for i in selected_columns]

    # -------------------------------------------------------------------------------------
