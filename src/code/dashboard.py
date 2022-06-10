from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output,State
from datetime import datetime

# Our modules
from dashboard_plots import * 
from dashboard_scorecard import *
from dashboard_components import *



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server




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





if __name__ == '__main__':
    app.run_server(debug=True)