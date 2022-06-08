import pandas as pd
from sklearn.preprocessing import StandardScaler
from dataPreProcessing import *


def normalize(dataframe):
    """ function to normalize dataframe"""
    data = dataframe.copy()
    scaler = StandardScaler()
    scaler.fit(dataframe)
    scaled_df = pd.DataFrame(scaler.transform(dataframe))
    scaled_df.index = data.index
    scaled_df.columns = data.columns
    return scaled_df


# function to get first difference (detrending)
def detrend(dataframe):
    return dataframe.diff().dropna()


# funtion to remove seasonality
def remove_seasonality(dataframe):
    data = dataframe.copy()
    # monthly mean
    mean_data = dataframe.groupby(dataframe.index.month).mean()
    for i, d in enumerate(data.index):
        data.iloc[i, :] = mean_data.loc[d.month]
    removed_seaonality_data = dataframe - data
    return removed_seaonality_data


# funtion to remove volatility
def remove_volatility(dataframe):
    data = dataframe.copy()
    # monthly mean
    std_data = dataframe.groupby(dataframe.index.year).std()
    for i, d in enumerate(data.index):
        data.iloc[i, :] = std_data.loc[d.year]
    removed_vol_data = dataframe - data
    return removed_vol_data

# predictors for lasso model

def get_lag1_data(corrcat, corrquery,retailsales_final, response_var='GrowthRate'):
    """ passed response dataframe and predictors' dataframe"""
    lasso_data = corrcat
    lasso_cat = remove_seasonality(detrend(normalize(lasso_data)))
    lasso_key = detrend(normalize(corrquery))
    

    # response
    lasso_response_var = retailsales_final[[response_var]].iloc[1:,:]

    # extract lag1 data to add to predictors
    lag1 = retailsales_final[[response_var]].iloc[0:retailsales_final.shape[0]-1,:]
    lag1.index = lasso_response_var.index
    lag1 = lag1.rename(columns={response_var: 'lag1'})
    lasso_predictors = make_predictors_df(lag1, lasso_key, lasso_cat)
    
    # extra test data
    predictors_with_extra = make_predictors_df(lasso_key, lasso_cat)
    extra_test_data = predictors_with_extra.loc[predictors_with_extra.index > lasso_predictors.index[len(lasso_predictors.index)-1], :]
    extra_test_data['lag1'] = lasso_response_var.iloc[-1][0]
    lasso_predictors = pd.concat([lasso_predictors, extra_test_data])
    return lasso_predictors, lasso_response_var


def get_lag1_data_ecommerce(retailEcommercesales_ts, ecommerce_keyword_ts, response_var='Growth_rate'):
    """ passed response dataframe and predictors' dataframe"""
    randomforest_key = detrend(normalize(ecommerce_keyword_ts))

    # response
    randomforest_response_var = retailEcommercesales_ts[[response_var]].iloc[1:,:]

    # extract lag1 data to add to predictors
    lag1 = retailEcommercesales_ts[[response_var]].iloc[0:retailEcommercesales_ts.shape[0]-1,:]
    lag1.index = randomforest_response_var.index
    lag1 = lag1.rename(columns={response_var: 'lag1'})
    randomforest_predictors = make_predictors_df(lag1, randomforest_key)

    # extra test data
    predictors_with_extra = make_predictors_df(randomforest_key)
    extra_test_data = predictors_with_extra.loc[predictors_with_extra.index > randomforest_predictors.index[len(randomforest_predictors.index)-1], :]
    extra_test_data['lag1'] = randomforest_response_var.iloc[-1][0]
    randomforest_predictors = pd.concat([randomforest_predictors, extra_test_data])
    return randomforest_predictors, randomforest_response_var