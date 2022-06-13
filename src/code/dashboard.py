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
                dbc.Col(html.Div(indicator),md=3, style = {'padding-right':'10px'}),
                dbc.Col(html.Div(year),md=8)
            ]), style = {'padding-bottom': '20px', 
                          'padding-left':'30px',
                          'padding-top':'20px'})

right_row2 = html.Div(dbc.Row(
            [
                dbc.Col(gdp_download_button),
                dbc.Col(rts_download_button),
                dbc.Col(ec_download_button),
                dbc.Col(about)
            ]), style = {'padding-bottom': '10px', 
                          'padding-left':'100px',
                          #'padding-right':'100px',
                          'padding-top':'5px'})


right_row3 = html.Div(dbc.Row([
    dbc.Col(growth_rate_plot_object),
    dbc.Col(card_growth_rate, width=3, style = {'padding-top': '140px', 'padding-bottom': '0px'})
]))


right_row4 = html.Div(dbc.Row([
    dbc.Col(value_plot_object),
    dbc.Col(card_value,  width=3, style = {'padding-top': '120px'})
]))


table_captions = dbc.Row([
    dbc.Col(html.Div("Table 1. Growth Rate and Value"), md = 4, style = {'text-align': "center"}),
    dbc.Col(html.Div("Table 2. Predicted Value with Prediction Interval"), md = 7, style = {'text-align': "center"})
])

right_row_5 = dbc.Row([
        dbc.Col(growth_rate_table, style = {'padding-left': '70px'}),
        dbc.Col(pred_interval_table, style = {'padding-right': '120px'})
    ])

right_row6 = dbc.Row([
    dbc.Col(actual_box,  md = 1, style = {'padding-left': '70px'}),
    dbc.Col(html.Div("Actual values"), md=2),
    dbc.Col(pred_box, md=1, style = {'padding-left': '70px'}),
    dbc.Col(html.Div("Predicted values"), md=2)
])


right_partition = html.Div(dbc.Col([
    right_row1,
    right_row2,
    right_row3,
    right_row4,
    html.Br(),
    table_captions,
    right_row_5, 
    html.Br(),
    right_row6
]))


row2 = html.Div(dbc.Row([
    dbc.Col(left_partition, md=2, style = {'background-color': '#47C1BF'}),
    dbc.Col(right_partition)
    ]))



################################ layout #############################################

app.layout = html.Div([
    row1,
    row2
], style = {'background-color': '#DFE4E8'})





if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')