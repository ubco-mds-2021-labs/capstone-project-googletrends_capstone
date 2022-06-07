import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA


def apply_dfm(predictor, num_factors=20, order_factors=1):
    model = sm.tsa.DynamicFactor(endog=predictor, k_factors=num_factors, factor_order=order_factors)
    res = model.fit()
    final = model.fit(res.params)
    factors = np.transpose(pd.DataFrame(final.factors.filtered))
    factors.index = predictor.index
    return factors


def fit_arima_model(train, dependent_var='GDP_GrowthRate', ar_order=1, ma_order=1):
    """ fits arma model to the training data set of GDP"""
    model = ARIMA(endog=train[dependent_var],
                  exog=train.loc[:, ~train.columns.isin([dependent_var])],
                  order=(ar_order, 0, ma_order))
    modelfit = model.fit(method='innovations_mle')
    return modelfit
