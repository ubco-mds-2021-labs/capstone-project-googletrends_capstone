import dash
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
import pathlib
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash import Dash, dash_table
from datetime import date
import math

dff = pd.read_csv('../../data/storeddata/Ecomm_GrowthRateResults.csv')
df=dff.tail(5)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dash_table.DataTable(df.to_dict('records'),
    style_table={'height': '100px'},
    style_cell={'textAlign': 'left'},
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'fontWeight': 'bold'
    }
    ,
    style_data_conditional=[
        {
            "if": {"row_index": len(df) - 1},
            "fontWeight": "bold",
            'backgroundColor': 'rgb(210, 210, 210)',
        },
    ],    
)

if __name__ == "__main__":
    app.run_server(debug=True)