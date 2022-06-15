from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from datetime import datetime
import pandas as pd

# Our modules
from src.code.dashboard_plots import * 
from src.code.dashboard_scorecard import *
from src.code.dashboard_components import *
from src.code.dashboard_callbacks import *
from src.code.dashboard_table_funs import *



# Row 1
row1 = html.Div(dbc.Row(header))

left_partition = html.Div([
                           html.Br(),
                           html.Div(html.Img(src='assets/trends_new.png', height='55px', width='75px'), style={'padding-left':'50px'}),
                           html.Br(),
                           html.H4("Quick Information"),
                           html.Br(),
                           html.H6(
    "The purpose of dashboard is to visualize nowcasting of economic indicators: Gross Domestic Product (GDP), Retail Trade Sales (RTS) and E-Commerce Sales (EC Sales)."),
                           html.Br(),
                           #html.H6("- The top two components are for you to adjust as per your need."),
                           #html.H6("- Select the indicator from the drop down to see the growth rate and indicator's value from the plots shown."),
                           #html.H6("- The GDP, RTS and EC Sales values are in 1,000,000s, 1,000s and 1,000s respectively."),
                           html.H6("- One step ahead prediction of indicators is shown on score cards"),
                           html.Br(),
                           html.H6("- More detailed predictions are expressed in Tables 1 and 2."),
                           html.Br(),
                           #html.H6("Visualize and observe the prediction interval"),
                           #html.H6("Capture predicted error obtained from the model fitting"),
                           #html.Br(),
                           #html.H6("- Capture indicator`s nowcasted growth rate and actual values."),
                           html.H6("- Click download buttons to get the keywords used for nowcasting."),
                           html.Br(),
                           #html.H6("- Also, the predicted growth rate and predicted value (one step ahead) can be seen towards the right of the plots!"),
                           #html.H6("- Adjust the slider to choose the year range and get the information accordingly."),
                           #html.H6("- The two plots are user friendly! The first one is for growth rate prediction of the indicator and the second one is for the predicted value."),
                           #html.H6("- Select the area to zoom in and use the options on the plot to explore more."),
                           html.H6("- For more information, click About button on top right corner!!"),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           html.H6("Data Sources: "),
                           html.Br(),
                           dcc.Markdown(
                        '''[Gross Domestic Product](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610010401)'''),
                           dcc.Markdown(
                        '''[Retail Trade Sales](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2010000802)'''),
                        dcc.Markdown(
                        '''[E - Commerce](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2010007201)'''),
                        dcc.Markdown(
                        '''[Google Trends](https://trends.google.com/trends/?geo=CA)'''),
                        dcc.Markdown(
                        '''[Github](https://github.com/ubco-mds-2021-labs/capstone-project-googletrends_capstone)'''),
                           html.Br(),
                           html.Br(),
                           html.Br(),
                           ],
    style={'background': '#B7ECEC', 'padding-left': '4%'})

right_partition = html.Div("this is right partition this is right partition ")  # overwritten later

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


right_row_caption = dbc.Row(right_row_captions)

right_row3 = html.Div(dbc.Row([
    dbc.Col(growth_rate_plot_object),
    dbc.Col(card_growth_rate, width=3, style = {'padding-top': '130px', 'padding-bottom': '0px'})
]))


right_row4 = html.Div(dbc.Row([
    dbc.Col(value_plot_object),
    dbc.Col(card_value,  width=3, style = {'padding-top': '105px'})
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
    right_row_caption,
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
    app.run_server(debug=True)
