import pandas as pd
import numpy as np
from tsModels import *


# function for rolling prediction of test and extra test set (GDP)
def rolling_prediction(train, test, extra_test, dependent_var='GDP_GrowthRate'):
    """ Rolling prediction for test set"""
    train_samples = train.shape[0]
    test_samples = test.shape[0]
    pred_data = pd.DataFrame(columns=None)

    # rolling prediction for testing set
    if not test.empty:
        for i in range(train_samples+1, train_samples+test_samples+1):
            modelfit = fit_arima_model(train)

            # Get first row of test set and make prediction
            firstrow_test = np.transpose(pd.DataFrame((test.iloc[0, :])))
            predicted_val = modelfit.forecast(step=1,
                            exog=firstrow_test.loc[:, ~firstrow_test.columns.isin([dependent_var])], 
                            dynamic=True)
            predicted_val = pd.DataFrame(predicted_val)
            pred_data = pred_data.append(predicted_val)

            # update training set with one row
            train = pd.concat([train, firstrow_test])

            # Drop first row from test set now
            test = test.drop(f"{firstrow_test.index[0]}")

    # rolling prediction for extra test set
    if not extra_test.empty:
        for i in range(0, extra_test.shape[0]):
            modelfit = fit_arima_model(train)

            # Get first row of extra test set and make prediction
            firstrow_test = np.transpose(pd.DataFrame((extra_test.iloc[0, :])))
            predicted_val = modelfit.forecast(step=1,
                            exog=firstrow_test.loc[:, ~firstrow_test.columns.isin([dependent_var])], 
                            dynamic=True)
            predicted_val = pd.DataFrame(predicted_val)
            firstrow_test['GDP_GrowthRate'] = predicted_val
            pred_data = pred_data.append(predicted_val)

            # update training set with one row
            train = pd.concat([train, firstrow_test])
            # Drop first row from test set now
            extra_test = extra_test.drop(f"{firstrow_test.index[0]}")


    return pred_data


def rolling_prediction_RF(train, test, extra_test, dependent_var='GrowthRate',n_trees=100):
    """ Rolling prediction for test set"""
    train_copy = train.copy()
    test_copy = test.copy()
    train_samples = train.shape[0]
    test_samples = test.shape[0]
    pred_data = pd.DataFrame(columns=None)

    # rolling prediction for testing set
    if not test.empty:
        for i in range(train_samples+1, train_samples+test_samples+1):
            modelfit = randomForest_modelfit(train,dependent_var, n_trees)

            # Get first row of test set and make prediction
            firstrow_test = np.transpose(pd.DataFrame((test.iloc[0, :])))
            predicted_val = modelfit.predict(firstrow_test.loc[:, ~firstrow_test.columns.isin([dependent_var])])
            predicted_val = pd.DataFrame(predicted_val)
            pred_data = pred_data.append(predicted_val)

            # update training set with one row
            train = pd.concat([train, firstrow_test])

            # Drop first row from test set now
            test = test.drop(f"{firstrow_test.index[0]}")

        pred_data.index = test_copy.index

    # rolling prediction for extra test set
    if not extra_test.empty:
        for i in range(0, extra_test.shape[0]):
            modelfit = randomForest_modelfit(train,dependent_var, n_trees)

            # Get first row of extra test set and make prediction
            firstrow_test = np.transpose(pd.DataFrame((extra_test.iloc[0, :])))
            firstrow_test['lag1'] = firstrow_test.tail(1)['lag1'][0]
            predicted_val = modelfit.predict(firstrow_test.loc[:, ~firstrow_test.columns.isin([dependent_var])])
            firstrow_test['GrowthRate'] = predicted_val[0]
            predicted_val = pd.DataFrame(predicted_val)
            pred_data = pred_data.append(predicted_val)
            pred_data.rename(index={0:extra_test.index[0]}, inplace=True)

            # update training set with one row
            train = pd.concat([train, firstrow_test])

            # Drop first row from test set now
            extra_test = extra_test.drop(f"{firstrow_test.index[0]}")


    return pred_data


def rolling_prediction_randomForest(train, test,extra_test, dependent_var='Growth_rate',n_trees=100):
    """ Rolling prediction for xgboost"""
    train_copy = train.copy()
    test_copy = test.copy()
    train_samples = train.shape[0]
    test_samples = test.shape[0]
    pred_data = pd.DataFrame(columns=None)

    # rolling prediction for testing set
    if not test.empty:
        for i in range(train_samples+1, train_samples+test_samples+1):
            modelfit = randomForest_modelfit(train, dependent_var, n_trees=n_trees)

            # Get first row of test set and make prediction
            firstrow_test = np.transpose(pd.DataFrame((test.iloc[0, :])))
            predicted_val = modelfit.predict(firstrow_test.loc[:, ~firstrow_test.columns.isin([dependent_var])])
            predicted_val = pd.DataFrame(predicted_val)
            pred_data = pred_data.append(predicted_val)

            # update training set with one row
            train = pd.concat([train, firstrow_test])

            # Drop first row from test set now
            test = test.drop(f"{firstrow_test.index[0]}")

        pred_data.index = test_copy.index

    # rolling prediction for extra test set
    if not extra_test.empty:
        for i in range(0, extra_test.shape[0]):
            modelfit = randomForest_modelfit(train, dependent_var, n_trees=n_trees)

            # Get first row of extra test set and make prediction
            firstrow_test = np.transpose(pd.DataFrame((extra_test.iloc[0, :])))
            firstrow_test['lag1'] = firstrow_test.tail(1)['lag1'][0]
            predicted_val = modelfit.predict(firstrow_test.loc[:, ~firstrow_test.columns.isin([dependent_var])])
            firstrow_test['Growth_rate'] = predicted_val[0]
            predicted_val = pd.DataFrame(predicted_val)
            pred_data = pred_data.append(predicted_val)
            pred_data.rename(index={0:extra_test.index[0]}, inplace=True)

            # update training set with one row
            train = pd.concat([train, firstrow_test])

            # Drop first row from test set now
            extra_test = extra_test.drop(f"{firstrow_test.index[0]}")

    return pred_data
