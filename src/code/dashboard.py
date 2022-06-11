from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from datetime import datetime
import pandas as pd

# Our modules
from dashboard_plots import * 
from dashboard_scorecard import *
from dashboard_components import *
from dashboard_callbacks import *
from dashboard_table_funs import *



# reset_button = html.Div([
#     dbc.Button("Reset", id="reset_btn",style={
#               #'background-color': 'blue',
#               'color': 'white',
#               'border': '0px',
#               'hover': { 
#                      'color': '#ffffff'
#               }
#       })
# ])


# Row 1
row1 = html.Div(dbc.Row(header))

left_partition = html.Div(" this is left side of partition")
right_partition = html.Div("this is right partition this is right partition this is right partition this is r this is right partition this is right partition this is right partitionight partition this is right partition")

right_row1 = html.Div(dbc.Row(
            [
                dbc.Col(html.Div(indicator),md=4),
                dbc.Col(html.Div(year),md=8)
            ]), style = {'padding-bottom': '20px'})

right_row2 = html.Div(dbc.Row(
            [
                dbc.Col(html.Div(gdp_download_button)),
                dbc.Col(html.Div(rts_download_button)),
                dbc.Col(html.Div(ec_download_button)),
                dbc.Col(html.Div(about))
            ]))


right_row3 = html.Div(dbc.Row([
    dbc.Col(growth_rate_plot_object),
    dbc.Col(card_growth_rate, width=2, style = {'padding-top': '150px',
                                                'padding-right': '0px',
                                                'right-margin': '10'})
]))


right_row4 = html.Div(dbc.Row([
    dbc.Col(value_plot_object),
    dbc.Col(card_value,  width=2, style = {'padding-top': '120px',
                                                'padding-right': '0px',
                                                'right-margin': '10'})
]))


right_row_5 = html.Div([
    dbc.Row(growth_rate_table),
    dbc.Row(pred_interval_table)
])


right_partition = html.Div(dbc.Col([
    right_row1,
    right_row2,
    right_row3,
    right_row4,
    right_row_5
]))

row2 = html.Div(dbc.Row([
    dbc.Col(left_partition, md=2),
    dbc.Col(right_partition)
    ]))


################################ layout #############################################

app.layout = dbc.Container([
    row1,
    row2
])





if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')