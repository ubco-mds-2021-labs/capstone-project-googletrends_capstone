from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from datetime import datetime
import pandas as pd

# Our modules
from dashboard_plots import *
from dashboard_scorecard import *
from dashboard_components import *
from dashboard_callbacks import *


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

left_partition = html.Div([html.Br(),
                           html.Br(),
                           html.H4("How to operate:"),

                           html.H6(
    "This dashboard is for nowcasting the economic indicators. The indicators that are used are Gross Domestic Product(GDP), Retail Trade Sales and E - commerce."),
                           html.H6("- The top two components are for you to adjust as per your need"),
                           html.H6("- Select the indicator from the drop down to see the growth rate and indicator's value from the plots shown."),
                           html.H6("- Also, the predicted growth rate and predicted value can be seen towards the right of the plots!"),
                           html.H6("- Adjust the slider to choose the year range and get the information accordingly."),
                           html.H6("- Keywords are used from the google trends. If you want to know the keywords which are used for the nowcasting, go ahead and download by clicking the buttons."),
                           html.H6("- The two plots are user friendly! The first one is for growth rate prediction of the indicator and the second one is for the predicted value."),
                           html.H6("- Select the area to zoom in and use the options on the plot for other informative options."),
                           html.H6("- If you want to know more about our project, go ahead and click the About button on the top right corner!"),
                           html.H6("Links: "),
                           html.Br()
                           ],
    style={'background': '#A9DFBF', 'padding-left': '4%'})
right_partition = html.Div(
    "this is right partition this is right partition this is right partition this is r this is right partition this is right partition this is right partitionight partition this is right partition")

right_row1 = html.Div(dbc.Row(
    [
        dbc.Col(html.Div(indicator), md=4),
        dbc.Col(html.Div(year), md=8)
    ]), style={'padding-bottom': '20px'})

right_row2 = html.Div(dbc.Row(
    [
        dbc.Col(html.Div(gdp_download_button)),
        dbc.Col(html.Div(rts_download_button)),
        dbc.Col(html.Div(ec_download_button)),
        dbc.Col(html.Div(about))
    ]))


right_row3 = html.Div(dbc.Row([
    dbc.Col(growth_rate_plot_object),
    dbc.Col(card_growth_rate, width=2, style={'padding-top': '150px',
                                              'padding-right': '0px',
                                              'right-margin': '10'})
]))


right_row4 = html.Div(dbc.Row([
    dbc.Col(value_plot_object),
    dbc.Col(card_value,  width=2, style={'padding-top': '120px',
                                         'padding-right': '0px',
                                         'right-margin': '10'})
]))


right_partition = html.Div(dbc.Col([
    right_row1,
    right_row2,
    right_row3,
    right_row4
]))

row2 = html.Div(dbc.Row([
    dbc.Col(left_partition, md=2),
    dbc.Col(right_partition)
]))


################################ layout #############################################

app.layout = html.Div([
    row1,
    row2
])


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
