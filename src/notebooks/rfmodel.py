import numpy as np
import pandas as pd
import statsmodels.api as sm

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error

from sklearn.ensemble import RandomForestRegressor

class rf_modelfit():
    def randomForest_modelfit(train_rf, dependent_var='Growth_rate',n_trees=100):
        """ fits Random Forest model to the passed data"""
        x_train, y_train = train_rf.loc[:, ~train_rf.columns.isin([dependent_var])], train_rf[[dependent_var]]
        RFmodel = RandomForestRegressor(n_estimators=n_trees)
        RFmodel.fit(x_train, y_train)
        return RFmodel
    
