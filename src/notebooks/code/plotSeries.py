import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import *
from statsmodels.tsa.arima.model import ARIMA


def plot_df(y, title="", xlabel='Date', ylabel='Value', dpi=100, width=16, height=5, markersize=2):
    """Function to plot the time series"""
    y.index = pd.to_datetime(y.index)
    fig = plt.figure(figsize=(width, height), dpi=dpi)
    plt.plot(y, marker='o', markersize=markersize)
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.close()
    return fig


def lag_plots(data):
    """plots acf and pacf plots"""
    plot_acf(data)
    plot_pacf(data)


# ARIMA residual plots
def arima_residual_plots(modelfit):
    """ Returns the residual plots of arima model fit when model fit argument is passed"""
    residuals = pd.DataFrame(modelfit.resid)
    fig, ax = plt.subplots(1, 2, figsize=(15, 4))
    residuals.plot(title="Residuals", ax=ax[0])
    residuals.plot(kind='kde', title='Density', ax=ax[1])
    plt.figure(figsize=(12, 5))
    plt.show()