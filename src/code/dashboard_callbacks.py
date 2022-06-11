from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output,State
from datetime import datetime
import pandas as pd

# Our modules
from dashboard_plots import * 
from dashboard_scorecard import *
from dashboard_components import *



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server


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
    

# for score card - Predicted growth rate
@app.callback(
    Output('pred_growth_rate_sc', 'children'),
    Input("indicators_dropdown", "value")
)
def update_indicator_growth_rate_scorecard(value):
    return indicator_growth_rate_scorecard(value)

# for score card - Predinted error
@app.callback(
    Output('pred_error', 'children'),
    Input("indicators_dropdown", "value")
)
def update_pred_error_scorecard(value):
    return pred_error_scorecard(value)
    

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

####################################### Downalod buttons callbakcs ##########################################
### GDP download button callback
@app.callback(
    Output("download-gdp-csv", "data"),
    Input("gdp_btn", "n_clicks"),
    prevent_initial_call=True,
)
def gdp_predictors_download(n_clicks):
    url = 'https://raw.githubusercontent.com/ubco-mds-2021-labs/capstone-project-googletrends_capstone/main/data/keywords_data/GDP.csv?token=GHSAT0AAAAAABQEJ7WG4WGHRLQYZQGFQ6RUYVDZNGA'
    gdp_df = pd.read_csv(url)
    return dcc.send_data_frame(gdp_df.to_csv, "GDPpredictors.csv")

### RTS download button callback
@app.callback(
    Output("download-rts-csv", "data"),
    Input("rts_btn", "n_clicks"),
    prevent_initial_call=True,
)
def rts_predictors_download(n_clicks):
    url = 'https://raw.githubusercontent.com/ubco-mds-2021-labs/capstone-project-googletrends_capstone/main/data/keywords_data/RETAIL_SALES.csv?token=GHSAT0AAAAAABQEJ7WHWQUC3NRHY7GPKNAIYVDVYZQ'
    rts_df = pd.read_csv(url)
    return dcc.send_data_frame(rts_df.to_csv, "RTSpredictors.csv")

### E-commerce download button callback
@app.callback(
    Output("download-ec-csv", "data"),
    Input("ec_btn", "n_clicks"),
    prevent_initial_call=True,
)
def ec_predictors_download(n_clicks):
    url = 'https://raw.githubusercontent.com/ubco-mds-2021-labs/capstone-project-googletrends_capstone/main/data/keywords_data/ECOMMERCE.csv?token=GHSAT0AAAAAABQEJ7WGK5KXX4UUUFUOJYTUYVDZU6A'
    ec_df = pd.read_csv(url)
    return dcc.send_data_frame(ec_df.to_csv, "ECommercepredictors.csv")
