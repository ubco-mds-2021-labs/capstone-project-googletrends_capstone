from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from datetime import datetime

# Our modules
from dashboard_plots import * 
from dashboard_scorecard import *



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server


# Header 
header =  html.Div(children=[
        html.Div([
            html.H1(children='Nowcasting Macroeconomic Indicators',
                    style = {'textAlign' : 'center','color':'#f5b942'}
            )],
            className='col-10',
            style = {'padding-top' : '1%'}
        ),
        
    ], style={'padding': 10, 'flex': 1})

# Description button
about = html.Div([
    html.Button('About', id='submit-val', n_clicks=0),
   
])

# Dropdown
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
    ], style={'padding': 10, 'flex': 1})


# year slider
max_year = int(pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year)
year =  html.Div(children=[
        html.Label('Select the year'),
        dcc.RangeSlider(min=2004, 
                        max=max_year,
                        id='year_slider',
                        value = [2004, max_year],
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
growth_rate_plot_object  = html.Div([dcc.Graph(
    id='growth_rate_plot',
    figure=indicator_growth_rate_plot(value='GDP', from_year=2004, 
                            end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year),
    style={'border-width': '0', 'width': '100%', 'height': '500px'})
])


# value plot object
value_plot_object  = html.Div([dcc.Graph(
    id='value_plot',
    figure=indicator_value_plot(value='GDP', from_year=2004, 
    end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year),
    style={'border-width': '0', 'width': '100%', 'height': '500px'})
])


# Row 1
row = html.Div(
    [
        dbc.Row(dbc.Col(header,md=10)),
        dbc.Row(
            [
                dbc.Col(html.Div(card_growth_rate),md=2),
                dbc.Col(html.Div(card_value),md=2),
                dbc.Col(html.Div(about),md=2),
                dbc.Col(html.Div(indicator),md=5),
                dbc.Col(html.Div(year),md=5),
                
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
        Input("year_slider", "value")
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
    



if __name__ == '__main__':
    app.run_server(debug=True)