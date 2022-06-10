from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output,State
from datetime import datetime

# Our modules
from dashboard_plots import * 
from dashboard_scorecard import *


################################ Header ################################
header =  html.Div(children=[
        html.Div([
            html.H1(children='Nowcasting Macroeconomic Indicators Using Google Trends',
                    style = {'textAlign' : 'center','color':'#f5b942'}
            )],
            #className='col-12',
            style = {'padding-top' : '1%'}
        ),
        
    ], style={'padding': 10, 'flex': 1})


################################ Dropdown ################################
indicator = html.Div(children=[
        html.Label('Select the Indicator'),
        dcc.Dropdown(
            id = 'indicators_dropdown',
            options=[
            {"label": "Gross Domestic Product", "value": "GDP"},
            {"label": "Retail Trade Sales", "value": "RTS"},
            {"label": "E-Commerce Sales", "value": "EC"}
        ],
        value='GDP'
        ),
    ])


################################ year slider ################################
max_year = int(pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year)
year =  html.Div(children=[
        html.Label('Select the year'),
        dcc.RangeSlider(min=2004, 
                        max=max_year,
                        id='year_slider',
                        value = [2004, max_year],
                        marks={i: str(i) for i in range(2004, max_year, 5)}),
    ])


############################ download buttons ##############################
# GDP Download button
gdp_download_button = html.Div([
    dbc.Button("Download GDP predictors", id="gdp_btn",style={
              #'background-color': 'blue',
              'color': 'white',
              'border': '0px',
              'hover': { 
                     'color': '#ffffff'
              }
      }),
    dcc.Download(id="download-gdp-csv")
])

# RTS Download button
rts_download_button = html.Div([
    dbc.Button("Download Retail Trade Sales predictors", id="rts_btn",style={
              #'background-color': 'blue',
              'color': 'white',
              'border': '0px',
              'hover': { 
                     'color': '#ffffff'
              }
      }),
    dcc.Download(id="download-rts-csv")
])

# EC Download button
ec_download_button = html.Div([
    dbc.Button("Download E-Commerce predictors", id="ec_btn",style={
              #'background-color': 'lightblue',
              'color': 'white',
              'border': '0px',
              'hover': { 
                     'color': 'blue'
              }
      }),
    dcc.Download(id="download-ec-csv")
])


################################ Description button ################################
about = html.Div(
    [
        dbc.Button("About", id="open-about"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Nowcasting Macroeconomic Indicators using Google Trends")),
                dbc.ModalBody("Wow this thing takes up a lot of space..."),
            ],
            id="modal-about",
            fullscreen=True,
        ),
    ]
)


################################ Score card for Growth rate ################################
card_growth_rate = html.Div(dbc.Card(
    [
        #dbc.CardHeader("Predicted Growth Rate (%)"),
        dbc.CardBody(
            [
                html.P("Predicted Growth Rate (%)", style = {"fontSize": "17px"}),
                html.P("Predicted growthrate is as shown below",
                       className="text-center", id="pred_growth_rate_sc", 
                       style = {"fontSize": "20px", 'font-weight':'bolder'})
            ]
        ),
    ],
    style={"width": "12rem", 'display': 'inline-block',
           "justify-content": "center", "border": "5px lightgray solid", 'text-align': "center"}
))


################################ Score card predicted value ################################
card_value = html.Div(dbc.Card(
    [
        #dbc.CardHeader("Predicted Value"),
        dbc.CardBody(
            [
                html.P("Predicted Value", style = {"fontSize": "17px"}),
                html.P("Predicted value is as shown below",
                       className="text-center", id="pred_value_sc", style = {"fontSize": "20px", 'font-weight':'bolder'}),
                html.P("Predicted Error (RMSE)",
                       className="text-center", style = {"fontSize": "15px"}),      
                html.P("Predicted error value",
                       className="text-center", id="pred_error", style = {"fontSize": "18px", 'font-weight':'bolder'})
            ]
        ),
    ],
    style={"width": "12rem", 'display': 'inline-block',
           "justify-content": "center", "border": "5px lightgray solid", 'text-align': "center"}
))


################################ Growth rate plot object ################################
growth_rate_plot_object  = html.Div([dcc.Graph(
    id='growth_rate_plot',
    figure=indicator_growth_rate_plot(value='GDP', from_year=2004, 
                            end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year),
    style={'border-width': '0', 'width': '100%', 'height': '500px'})
])


################################ value plot object ################################
value_plot_object  = html.Div([dcc.Graph(
    id='value_plot',
    figure=indicator_value_plot(value='GDP', from_year=2004, 
    end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year),
    style={'border-width': '0', 'width': '100%', 'height': '500px'})
])