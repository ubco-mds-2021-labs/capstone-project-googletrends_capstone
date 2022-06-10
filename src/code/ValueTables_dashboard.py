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

GrowthRateResults = pd.read_csv('../../data/storeddata/Ecomm_ValueResults.csv')
GrowthRateResults = GrowthRateResults.tail(5)

for i in range(len(GrowthRateResults)):
    
    if math.isnan(GrowthRateResults.iloc[i,1]):
        GrowthRateResults.iloc[i,1] = GrowthRateResults.iloc[i,3]
    
GrowthRateResults_Table = GrowthRateResults.iloc[:,[0,1,4,5,6]]
GrowthRateResults_Table.rename(columns={list(GrowthRateResults_Table)[0]:'Date'}, inplace=True)
GrowthRateResults_Table.rename(columns={list(GrowthRateResults_Table)[2]:'Prediction Interval (2.5%)'}, inplace=True)
GrowthRateResults_Table.rename(columns={list(GrowthRateResults_Table)[3]:'Prediction Interval (97.5%)'}, inplace=True)
#GrowthRateResults_Table = GrowthRateResults_Table.set_index('Date')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dash_table.DataTable(GrowthRateResults_Table.to_dict('records'),
    style_table={'height': '400px','width': '800px'},
    #style_cell={'textAlign': 'left'},
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'fontWeight': 'bold'
    },
    style_data_conditional=[
        {
            "if": {"row_index": len(GrowthRateResults_Table) - 1},
            "fontWeight": "bold",
            'backgroundColor': 'rgb(210, 210, 210)',
        }
    ],
    style_cell={
        'textAlign': 'center',
        'height': '400',
        'width': '800px',
        # all three widths are needed
        'minWidth': '70px', 'width': '110px', 'maxWidth': '260px',
        'whiteSpace': 'normal'
    }
    
)

if __name__ == "__main__":
    app.run_server(debug=True)