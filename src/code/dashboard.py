from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from datetime import datetime

# Our modules
from dashboard_plots import *
from dashboard_scorecard import *


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server


# Header
header = html.Div(children=[
    html.Div([
        html.H1(children='Nowcasting Macroeconomic Indicators',
                style={'textAlign': 'center', 'color': '#f5b942'}
                )],
             className='col-10',
             style={'padding-top': '1%'}
             ),

], style={'padding': 10, 'flex': 1})

# Description button
about = html.Div(
    [
        dbc.Button("About", id="open-about"),
        dbc.Modal(
            [
                # Title
                dbc.ModalHeader(dbc.ModalTitle(html.Div([
                    html.H1(children='Nowcasting Macroeconomic Indicators using Google Trends',
                            style={'color': '#935116 '}
                            ),
                    # html.Img(src='/../../assets/ubc.png')
                ],

                    style={'padding-top': '1%'}
                ),)),

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
                               "justify-content": "center", "border": "5px lightgray solid", 'background': '#FDF2E9'}
                    ),
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
                               "justify-content": "center", "border": "5px lightgray solid", 'background': '#FDF2E9'}
                    ),
                    html.Br(),
                    html.Br(),


                ], style={'padding-top': '1%', 'padding-left': '2%', 'padding-right': '2%', "background": "#D6EAF8"}),



            ],
            id="modal-about",
            fullscreen=True,
        ),
    ]
)

# Dropdown
indicator = html.Div(children=[
    html.Label('Select the Indicator'),
    dcc.Dropdown(
        id='indicators_dropdown',
        options=[
            {"label": "Gross Domestic Product", "value": "GDP"},
            {"label": "Retail Trade Sales", "value": "RTS"},
            {"label": "E-Commerce Sales", "value": "EC"}
        ],
        value='GDP'
    ),
], style={'padding': 10, 'flex': 1})


# year slider
max_year = int(pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year)
year = html.Div(children=[
    html.Label('Select the year'),
    dcc.RangeSlider(min=2004,
                    max=max_year,
                    id='year_slider',
                    value=[2004, max_year],
                    marks={i: str(i) for i in range(2004, max_year, 5)}),
], style={'padding': 10, 'flex': 1})


# Score card for Growth rate predicted Growth rate
card_growth_rate = dbc.Card(
    [
        dbc.CardHeader("Predicted Growth Rate (%)"),
        dbc.CardBody(
            [
                html.P("Predicted growthrate is as shown below",
                       className="text-center", id="pred_growth_rate_sc")
            ]
        ),
    ],
    style={"width": "10rem", 'display': 'inline-block',
           "justify-content": "center", "border": "5px lightgray solid"}
)


# Score card for Growth rate predicted value
card_value = dbc.Card(
    [
        dbc.CardHeader("Predicted Value"),
        dbc.CardBody(
            [
                html.P("Predicted value is as shown below",
                       className="text-center", id="pred_value_sc"),
                html.P("Predicted error",
                       className="text-center", id="pred_error")
            ]
        ),
    ],
    style={"width": "10rem", 'display': 'inline-block',
           "justify-content": "center", "border": "5px lightgray solid"}
)


# Growth rate plot object
growth_rate_plot_object = html.Div([dcc.Graph(
    id='growth_rate_plot',
    figure=indicator_growth_rate_plot(value='GDP', from_year=2004,
                                      end_year=pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year),
    style={'border-width': '0', 'width': '100%', 'height': '500px'})
])


# value plot object
value_plot_object = html.Div([dcc.Graph(
    id='value_plot',
    figure=indicator_value_plot(value='GDP', from_year=2004,
                                end_year=pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year),
    style={'border-width': '0', 'width': '100%', 'height': '500px'})
])


# Row 1
row = html.Div(
    [
        dbc.Row(dbc.Col(header, md=10)),
        dbc.Row(
            [
                dbc.Col(html.Div(card_growth_rate), md=2),
                dbc.Col(html.Div(card_value), md=2),
                dbc.Col(html.Div(about), md=2),
                dbc.Col(html.Div(indicator), md=5),
                dbc.Col(html.Div(year), md=5),

            ]
        ),
    ]
)

################################ layout #############################################

app.layout = dbc.Container([
    row,
    growth_rate_plot_object,
    value_plot_object
])


########################## Callbacks #############################################
# for growth rate plot
@app.callback(
    Output("growth_rate_plot", 'figure'),
    [
        Input("indicators_dropdown", "value"),
        Input("year_slider", "value")
    ]
)
def update_indicator_growth_rate_plot(value, year):
    from_year = year[0]
    end_year = year[1]
    return indicator_growth_rate_plot(value, from_year, end_year)

# for value plot


@app.callback(
    Output("value_plot", 'figure'),
    [
        Input("indicators_dropdown", "value"),
        Input("year_slider", "value"),
    ]
)
def update_indicator_value_plot(value, year):
    from_year = year[0]
    end_year = year[1]
    return indicator_value_plot(value, from_year, end_year)


# for score card - Predicted value
@app.callback(
    Output('pred_value_sc', 'children'),
    Input("indicators_dropdown", "value")
)
def update_indicator_value_scorecard(value):
    return indicator_value_scorecard(value)


# for score card - Predinted growth rate
@app.callback(
    Output('pred_growth_rate_sc', 'children'),
    Input("indicators_dropdown", "value")
)
def update_indicator_growth_rate_scorecard(value):
    return indicator_growth_rate_scorecard(value)


# Call back for About
@app.callback(
    Output("modal-about", "is_open"),
    Input("open-about", "n_clicks"),
    State("modal-about", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
