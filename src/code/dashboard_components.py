from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
from datetime import datetime

# Our modules
from dashboard_plots import * 
from dashboard_scorecard import *
from dashboard_table_funs import *


################################ Header ################################
header =  html.Div(children=[
        html.Div([
                    dbc.Row([
                    dbc.Col(html.Div(html.Img(src='assets/ca-flag.jpg', height='60px', width='100px'), style={"padding-left":'30px'}), md=1),
                    dbc.Col([
                        dbc.Row(html.H1(children='Nowcasting Macroeconomic Indicators Using Google Trends',
                        style = {'textAlign' : 'center','color':'white'})),
                        dbc.Row(html.H3(children='Statistics Canada',
                        style = {'textAlign' : 'center','color':'white'}))]
                    , md=10
                    ),
                    dbc.Col(html.Div(html.Img(src='assets/ubc.png', height='80px', width='80px'), style={"padding-right":'0px'}), md=1)
                ],
            #className='col-12',
            style = {'padding-top' : '1%'}
        ),
        ]),
    ], style = {'background-color': '#00848E'})


################################ Dropdown ################################
indicator = html.Div(children=[
        html.Label('Select the Indicator'),
        dcc.Dropdown(
            id = 'indicators_dropdown',
            options=[
            {"label": "Gross Domestic Product (GDP)", "value": "GDP"},
            {"label": "Retail Trade Sales (RTS)", "value": "RTS"},
            {"label": "E-Commerce Sales (EC Sales)", "value": "EC"}
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
                        marks={i: str(i) for i in range(2004, max_year, 5)}, 
                        tooltip={"placement": "bottom", "always_visible": True}),
    ])


############################ download buttons ##############################
# GDP Download button
gdp_download_button = html.Div([
    dbc.Button("Download GDP predictors", id="gdp_btn", color = 'secondary', style={
              #'background-color': '#47C1BF',
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
    dbc.Button("Download RTS predictors", id="rts_btn", color = 'secondary', style={
              #'background-color': '#47C1BF',
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
    dbc.Button("Download EC Sales predictors", id="ec_btn",color = 'secondary', style={
              #'background-color': '#47C1BF',
              'color': 'white',
              'border': '0px',
              'hover': { 
                     'color': 'blue'
              }
      }),
    dcc.Download(id="download-ec-csv")
])


################################ Score card for Growth rate ################################
card_growth_rate = html.Div(dbc.Card(
    [
        #dbc.CardHeader("Predicted Growth Rate (%)"),
        dbc.CardBody(
            [
                html.P("Date",
                       className="text-center", id="date_growth_rate", 
                       style = {"fontSize": "20px", 'font-weight':'bolder'}),
                html.P("Predicted Growth Rate (%)", style = {"fontSize": "17px"}),
                html.P("Predicted growthrate is as shown below",
                       className="text-center", id="pred_growth_rate_sc", 
                       style = {"fontSize": "20px", 'font-weight':'bolder'})
            ]
        ),
    ],
    style={"width": "12rem", 'display': 'inline-block',
           "justify-content": "center", 
           "border": "3px solid #47C1BF", 
           'text-align': "center", 
           "color": "#003135",
           "background-color": "#B7ECEC"}
))


################################ Score card predicted value ################################
card_value = html.Div(dbc.Card(
    [
        #dbc.CardHeader("Predicted Value"),
        dbc.CardBody(
            [
                html.P("Date",
                       className="text-center", id="date_value", 
                       style = {"fontSize": "20px", 'font-weight':'bolder'}),
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
           "justify-content": "center", 
           "border": "3px solid #47C1BF", 
           'text-align': "center", 
           "color": "#003135",
           "background-color": "#B7ECEC"}
))


################################ Growth rate plot object ################################
growth_rate_plot_object  = html.Div([dcc.Graph(
    id='growth_rate_plot',
    figure=indicator_growth_rate_plot(value='GDP', from_year=2004, 
                            end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year),
    style={'border-width': '0', 'width': '100%', 'padding-left': '40px'})
])


################################ value plot object ################################
value_plot_object  = html.Div([dcc.Graph(
    id='value_plot',
    figure=indicator_value_plot(value='GDP', from_year=2004, 
    end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year),
    style={'border-width': '0', 'width': '100%', 'padding-left': '40px'})
])


################################ Description button ################################
# Description button
about = html.Div(
    [
        dbc.Button("About", id="open-about", color = 'secondary', style={
              #'background-color': '#47C1BF',
              'color': 'white',
              'border': '0px',
              'hover': { 
                     'color': '#ffffff'
              }
      }),
        dbc.Modal(
            [
                # Title
                dbc.ModalHeader(dbc.ModalTitle(html.Div([
                    html.H1(children='Nowcasting Macroeconomic Indicators using Google Trends',
                            style={'color': 'white'}
                            ),
                    # html.Img(src='/../../assets/ubc.png')
                ],

                    style={'padding-top': '1%'}
                ),), style = {'background-color': '#00848E'}),

                # Content
                html.Div([

                    # Overview
                    html.H4(children='Overview'),
                    html.H6(children='Macroeconomic factors are the key drivers of economy, and their timely information helps in good policy making. However, this information is available with a lag, for instance, the data for the present month’s GDP is generally published in the coming month/quarter which causes delay in decision-making. To overcome this issue of delayed information gave rise to nowcasting approach. This is what this project will serve. This project nowcasts the macroeconomic factors and uses the keywords from Google Trends to predict the indicators.'),
                    html.Br(),

                    # Description of indicators and Google Trends
                    html.H4(children='Our Indicators and Predictors'),
                    html.H6(
                        children='Data set for this project are open ended and the short description about data is provided below:'),
                    html.H6(children='1. Gross Domestic Product (GDP):',  style={
                            "font-size": "20px", "text-decoration": "underline", "color": "red"}),
                    html.H6(
                        children='This dataset is a comma separated file containing the information about the monthly GDP. Link of file is as below:'),
                    dcc.Markdown(
                        '''[Gross Domestic Product](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610010401)'''),
                    html.H6(children='2. Retail Trade Sales:',  style={
                            "font-size": "20px", "text-decoration": "underline", "color": "#F5B041 "}),
                    html.H6(children='This is a comma separated data set containing the information about the retail sales trades as per the industry. Link of file is as below:'),
                    dcc.Markdown(
                        '''[Retail Trade Sales](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2010000802)'''),
                    html.H6(children='3. E - Commerce:',  style={
                            "font-size": "20px", "text-decoration": "underline", "color": "green"}),
                    html.H6(
                        children='This is a comma separated dataset containing the information about the retail e-commerce sales. Link of file is as below:'),
                    dcc.Markdown(
                        '''[E - Commerce](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2010007201)'''),
                    html.H6(children='4. Google Trends API:',  style={
                            "font-size": "20px", "text-decoration": "underline", "color": "#2980B9"}),
                    html.H6(children='We have accessed Google Trends website to get real time data for the macroeconomic indicators. Different keywords, categories and subcategories are used to extract Google Trends predictors such as Economic crisis, loans, GPS, unemployment, affordable housing, economy news, agriculture, and forestry. Link of file is as below:'),
                    dcc.Markdown(
                        '''[Google Trends](https://trends.google.com/trends/?geo=CA)'''),

                    # Info on nowcasting
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H2("Why is it Nowcasting and not Forecasting?")),
                            dbc.CardBody(
                                [
                                    html.H5("Nowcast: Predicting the present. This project takes the present data and use that data to predict the values for indicators in present. Rather than predicting the future, we are predicting the present for the indicators.",
                                            className="text-center")
                                ]
                            ),
                        ],

                        style={"width": "42rem", 'display': 'inline-block',
                               "justify-content": "center", "border": "5px #00848E solid", 'background': '#DFE4E8'}
                    ),
                        ]),
                        dbc.Col([
                            dbc.Card(
                        [
                            dbc.CardHeader(
                                html.H2("Why do we use Google Trends data?")),
                            dbc.CardBody(
                                [
                                    html.H5("Google trends provide the keywords which are used as predictors in nowcasting the indicators. Trend is used for a particular keyword which is number of searches for that keyword per total number of searches.",
                                            className="text-center")
                                ]
                            ),
                        ],
                        style={"width": "42rem", 'display': 'inline-block',
                               "justify-content": "center", "border": "5px #00848E solid", 'background': '#DFE4E8'}
                    )
                        ])
                    ]), 
                    html.Br(),
                    html.Br(),

                ], style={'padding-top': '2%', 'padding-left': '3%', 'padding-right': '2%', "background": "#E0F5F5"}),



            ],
            id="modal-about",
            fullscreen=True,
        ),
    ]
)


####################### Small Table #########################################
growth_rate_table = html.Div(dash_table.DataTable(GrowthValueTable('GDP').to_dict('records'),
), id = 'growth_table')


############################# Prediction interval table ##############################
pred_interval_table = html.Div(dash_table.DataTable(ValueTable('GDP').to_dict('records')),
id = 'pred_int_table')


############### pred and actual boxes ########################
pred_box = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div("")
            ]
        ),
    ],
    style={"width": "2rem", "height": "2rem", 'display': 'inline-block',
           "border": "1px solid #47C1BF", 
           "background-color": "#B7ECEC"}
)

actual_box = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div("")
            ]
        ),
    ],
    style={"width": "2rem", "height": "2rem", 'display': 'inline-block',
           "border": "1px solid darkgrey", 
           "background-color": "white"}
)

