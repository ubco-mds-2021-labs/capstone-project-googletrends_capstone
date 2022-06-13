import pandas as pd
import plotly.graph_objects as go
from datetime import datetime



### Read data for all the indicators (value)
gdp_value_path = '../../data/storeddata/GDP_ValueResults.csv'
gdp_value = pd.read_csv(gdp_value_path, index_col=0)
gdp_value.index = pd.to_datetime(gdp_value.index)
rts_value_path = '../../data/storeddata/RTS_ValueResults.csv'
rts_value = pd.read_csv(rts_value_path, index_col=0)
rts_value.index = pd.to_datetime(rts_value.index)
ec_value_path = '../../data/storeddata/EComm_ValueResults.csv'
ec_value = pd.read_csv(ec_value_path, index_col=0)
ec_value.index = pd.to_datetime(ec_value.index)

### Read data for all the indicators (Growth Rate)
gdp_growth_path = '../../data/storeddata/GDP_GrowthRateResults.csv'
gdp_growth = pd.read_csv(gdp_growth_path, index_col=0)
gdp_growth.index = pd.to_datetime(gdp_growth.index)
gdp_growth = gdp_growth.rename(columns={'GDP_GrowthRate': 'Actual Growth Rate'})
rts_growth_path = '../../data/storeddata/RTS_GrowthRateResults.csv'
rts_growth = pd.read_csv(rts_growth_path, index_col=0)
rts_growth.index = pd.to_datetime(rts_growth.index)
rts_growth = rts_growth.rename(columns={'GrowthRate': 'Actual Growth Rate'})
ec_growth_path = '../../data/storeddata/EComm_GrowthRateResults.csv'
ec_growth = pd.read_csv(ec_growth_path, index_col=0)
ec_growth.index = pd.to_datetime(ec_growth.index)
ec_growth = ec_growth.rename(columns={'Ecommerce_GrowthRate': 'Actual Growth Rate'})


def value_plot(data, actual_name, fitted_name, predicted_name, y_title, x_title, plot_title):
    """function to make plot of given data"""
    fig = go.Figure()

    # Actual value
    fig.add_trace(
        go.Scatter(
            name="Actual value",
            x=data.index,
            y=data[actual_name]
        ))
    # Fitted value
    fig.add_trace(
        go.Scatter(
            name="Fitted value",
            x=data.index,
            y=data[fitted_name]
        ))
    # Predicted value
    fig.add_trace(
        go.Scatter(
            name='Predicted value (rolling)',
            x=data.index,
            y=data[predicted_name],
            line=dict(color="#00848E")
        ))
    # Upper bound
    fig.add_trace(
        go.Scatter(
            name='Upper bound',
            x=data.index,
            y=data['0.975'],
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ))
    # lower bound
    fig.add_trace(
        go.Scatter(
            name='lower bound',
            x=data.index,
            y=data['0.025'],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(48,213,200,0.5)',  # grey color 'rgba(68, 68, 68, 0.3)', darkgreen rgba(0,100,0,0.4)
            fill='tonexty',
            showlegend=False
        ))
    # Mean of prediction interval
    fig.add_trace(
        go.Scatter(
            name="Mean (Prediction interval)",
            x=data.index,
            y=data['Mean (Prediction invertal)'],
            line=dict(color="#00848E", dash='dot', width=3)
        ))

    fig.update_layout(
        yaxis_title=y_title,
        xaxis_title=x_title,
        title={
        'text': plot_title,
        'x':0.08,
        'xanchor': 'left',
        'yanchor': 'top'},
        hovermode="x",
        width=900,
        height=400,
        legend={'traceorder':'normal',
                'orientation': 'h',
                'yanchor': "bottom",
                'y': 1,
                'xanchor': "right",
                'x': 1},
        margin=dict(
        b=10, # bottom margin: 10px
        l=10, # left margin: 10px
        r=2 # right margin: 10px
    ),
    # trasparent-background
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor= 'rgba(0,0,0,0)',
    xaxis = dict(showline = True, linecolor = 'black', linewidth=1),
    yaxis = dict(showline = True, linecolor = 'black', linewidth=1)
    )
    return fig


def indicator_value_plot(value='GDP', from_year=2004, end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year):
    """ function selects required data and returns the desired indicator's value plot for provided year range"""
    if value == 'GDP':
        data = gdp_value
        actual_name = "Actual GDP"
        fitted_name = "Fitted GDP"
        predicted_name = "Predicted GDP"
        y_title='GDP'
        x_title='Timeline (Quarters)'
        plot_title='Gross Domestic Product (GDP) Prediction'
            
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        fig = value_plot(data, actual_name, fitted_name, predicted_name, y_title, x_title, plot_title)

    elif value == 'RTS':
        data = rts_value
        actual_name = "Actual Retail Sales"
        fitted_name = "Fitted Retail Sales"
        predicted_name = "Predicted Retail Sales"
        y_title='Retail Trade Sales'
        x_title='Timeline (Months)'
        plot_title='Retail Trade Sales Prediction'
            
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        fig = value_plot(data, actual_name, fitted_name, predicted_name, y_title, x_title, plot_title)

    elif value == 'EC':
        data = ec_value
        actual_name = "Actual Ecommerce"
        fitted_name = "Fitted Ecommerce"
        predicted_name = "Predicted Ecommerce"
        y_title='E-Commerce Trade Sales'
        x_title='Timeline (Months)'
        plot_title='E-Commerce Trade Sales Prediction'
            
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        fig = value_plot(data, actual_name, fitted_name, predicted_name, y_title, x_title, plot_title)
    return fig


def indicator_growth_rate_plot(value='GDP', from_year=2004, end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year):
    """ function selects required data and returns the desired indicator's value plot for provided year range"""

    actual_name = "Actual Growth Rate"
    fitted_name = "Fitted Value"
    predicted_name = "Predicted Value"

    if value == 'GDP':
        data = gdp_growth
        y_title='GDP Growth Rate (%)'
        x_title='Timeline (Quarters)'
        plot_title='Gross Domestic Product (GDP) Growth Rate Prediction'
            
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        fig = value_plot(data, actual_name, fitted_name, predicted_name, y_title, x_title, plot_title)

    elif value == 'RTS':
        data = rts_growth
        y_title='Retail Trade Sales Growth Rate (%)'
        x_title='Timeline (Months)'
        plot_title='Retail Trade Sales Growth Rate Prediction'
            
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        fig = value_plot(data, actual_name, fitted_name, predicted_name, y_title, x_title, plot_title)

    elif value == 'EC':
        data = ec_growth
        y_title='E-Commerce Trade Sales Growth Rate (%)'
        x_title='Timeline (Months)'
        plot_title='E-Commerce Trade Sales Growth Rate Prediction'
            
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        fig = value_plot(data, actual_name, fitted_name, predicted_name, y_title, x_title, plot_title)
    return fig