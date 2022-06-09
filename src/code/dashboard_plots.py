import pandas as pd
import plotly.graph_objects as go
from datetime import datetime



### Read data for all the indicators
gdp_value_path = '../../data/storeddata/GDP_ValueResults.csv'
gdp_value = pd.read_csv(gdp_value_path, index_col=0)
gdp_value.index = pd.to_datetime(gdp_value.index)
rts_value_path = '../../data/storeddata/RTS_ValueResults.csv'
rts_value = pd.read_csv(rts_value_path, index_col=0)
rts_value.index = pd.to_datetime(rts_value.index)
ec_value_path = '../../data/storeddata/EComm_ValueResults.csv'
ec_value = pd.read_csv(ec_value_path, index_col=0)
ec_value.index = pd.to_datetime(ec_value.index)


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
            line=dict(color="darkgreen")
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
            fillcolor='rgba(0,100,0,0.4)',  # grey color 'rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        ))
    # Mean of prediction interval
    fig.add_trace(
        go.Scatter(
            name="Mean (Prediction interval)",
            x=data.index,
            y=data['Mean (Prediction invertal)'],
            line=dict(color="darkgreen", dash='dot', width=3)
        ))

    fig.update_layout(
        yaxis_title=y_title,
        xaxis_title=x_title,
        title=plot_title,
        hovermode="x",
        width=1100,
        height=450,
        legend={'traceorder':'normal'}
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