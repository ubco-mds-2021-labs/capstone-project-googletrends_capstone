from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Our modules
from dashboard_plots import * 


fig1 = indicator_value_plot(value='GDP', from_year=2004, end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year)
fig2 = indicator_growth_rate_plot(value='GDP', from_year=2004, end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year)

#app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server



header =  html.Div(children=[
        html.Div([
            html.H1(children='Nowcasting Macroeconomic Indicators',
                    style = {'textAlign' : 'center','color':'#f5b942'}
            )],
            className='col-10',
            style = {'padding-top' : '1%'}
        ),
        
    ], style={'padding': 10, 'flex': 1})

about = html.Div([
    html.Button('About', id='submit-val', n_clicks=0),
   
])

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

year =  html.Div(children=[
        html.Label('Select the year'),
        dcc.RangeSlider(min=2004, max=2022,value = [2004, 2022], marks={i: str(i) for i in range(2004, 2022, 5)},id = 'year'),
    ], style={'padding': 10, 'flex': 1})



row = html.Div(
    [
        dbc.Row(dbc.Col(header,md=10)),
        dbc.Row(
            [
                dbc.Col(html.Div(about),md=2),
                dbc.Col(html.Div(indicator),md=5),
                dbc.Col(html.Div(year),md=5),
                
            ]
        ),
    ]
)



app.layout = html.Div([
    row
     
], style={'display': 'flex', 'flex-direction': 'row'})

if __name__ == '__main__':
    app.run_server(debug=True)