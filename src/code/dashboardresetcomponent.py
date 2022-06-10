import dash
import pandas as pd
import dash_bootstrap_components as dbc
import pathlib
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash import Dash, dash_table
from datetime import date



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

bttn = html.Div(
    [
        dbc.Button("Reset", id="reset-button"),
        
    ]
)

text_box = html.Div(
    [
        dcc.Input(
            id="input_{}".format(_),
            type=_,
            placeholder="input type {}".format(_),
        )
        for _ in ALLOWED_TYPES
    ]
    + [html.Div(id="out-all-types")]
)

app.layout = dbc.Container([
    text_box,
    bttn
])

if __name__ == "__main__":
    app.run_server(debug=True)