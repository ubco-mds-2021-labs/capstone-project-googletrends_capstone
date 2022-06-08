import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor


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

def randomForest_modelfit(train_rf, response_var='GrowthRate', n_trees = 1000):
    """ fits Random Forest model to the passed data"""
    x_train, y_train = train_rf.loc[:, ~train_rf.columns.isin([response_var])], train_rf[[response_var]]
    RFmodel = RandomForestRegressor(n_estimators=n_trees)
    RFmodel.fit(x_train, y_train)
    return RFmodel

