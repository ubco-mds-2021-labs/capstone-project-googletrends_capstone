import numpy as np
import pandas as pd
import statsmodels.api as sm

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class processing():
    def get_long_term_trend(dataframe, freq='M'):
        """extract the monthly trend from the series"""
        dataframe = np.log(dataframe)
        long_term_trend_data = dataframe.copy()
        if freq == 'Q':
            lamb = 1600
        elif freq == 'M':
            lamb = 1600*3**4
        for column_name in dataframe.columns:
            cycle, trend = sm.tsa.filters.hpfilter(dataframe[column_name], lamb)
            long_term_trend_data[column_name] = trend
        return long_term_trend_data


    def remove_downward_trend_bias(dataframe, gdp_categoryts_df, freq = 'M'):
        """pass dataframe to remove bias and downward trend"""
        trend_data = get_long_term_trend(gdp_categoryts_df, freq)
        log_category = np.log(dataframe)
        log_category.replace([np.inf, -np.inf], 0, inplace=True)
        avg_logcategory = log_category.mean()
        pca = PCA(n_components=1)
        pca.fit(trend_data)
        component = pd.DataFrame(pca.fit_transform(trend_data))

        # rescale component
        # transformation source link: https://stats.stackexchange.com/questions/46429/transform-data-to-desired-mean-and-standard-deviation
        rescaled_component = avg_logcategory.mean() + (component - component.mean())*(avg_logcategory.std()/component.std())

        # remove long term bias
        transformed_data = log_category - rescaled_component.values
        transformed_data.index = pd.to_datetime(transformed_data.index)

        return transformed_data

    def normalize(dataframe):
        """function to normalize dataframe"""
        data = dataframe.copy()
        scaler = StandardScaler()
        scaler.fit(dataframe)
        scaled_df = pd.DataFrame(scaler.transform(dataframe))
        scaled_df.index = data.index
        scaled_df.columns = data.columns
        return scaled_df

    # difference
    def detrend(dataframe):
        """function to detrend time series"""
        return dataframe.diff().dropna()

    # seasonality
    def remove_seasonality(dataframe):
        """function for differencing of time series"""
        data = dataframe.copy()
        # monthly mean
        mean_data = dataframe.groupby(dataframe.index.month).mean()

        for i, d in enumerate(data.index):
            data.iloc[i,:] = mean_data.loc[d.month]
        removed_seaonality_data = dataframe - data
        return removed_seaonality_data

    # cyclicity 
    def remove_volatility(dataframe):
        """function for removing volatility of time series"""
        data = dataframe.copy()
        # monthly mean
        std_data = dataframe.groupby(dataframe.index.year).std()
        for i, d in enumerate(data.index):
            data.iloc[i,:] = std_data.loc[d.year]
        removed_vol_data = dataframe - data
        return removed_vol_data

    def make_predictors_df(*arg):
        """joins the predictors dataframes"""
        if len(arg) > 1:
            for i in range(0, len(arg)-1):
                if i == 0:
                    arg[i].index = pd.to_datetime(arg[i].index)
                    arg[i+1].index = pd.to_datetime(arg[i+1].index)
                    predictors_df = pd.merge(arg[i], arg[i+1], left_index=True, right_index=True)
                else:
                    predictors_df = pd.merge(predictors_df, arg[i+1], left_index=True, right_index=True)
        else:
            arg[0].index = pd.to_datetime(arg[0].index)
            return arg[0]
        return predictors_df

    def ts_train_test_split(response, predictor, test_size):
        " splits the train and test set and also returns the extra test data of predictors"
        # train test split
        joind_df = pd.merge(response, predictor, left_index=True, right_index=True)
        train, test = train_test_split(joind_df, test_size=test_size, shuffle=False)
        # extra test data
        extra_test_data = predictor.loc[predictor.index > joind_df.index[len(joind_df.index)-1], :]
        return train, test, extra_test_data

class lag(processing):
    def get_lag1_data(retailEcommercesales_ts, ecommerce_keyword_ts, response_var='Growth_rate'):
        """ passed response dataframe and predictors' dataframe"""
        randomforest_key = processing.detrend(processing.normalize(ecommerce_keyword_ts))

        # response
        randomforest_response_var = retailEcommercesales_ts[[response_var]].iloc[1:,:]

        # extract lag1 data to add to predictors
        lag1 = retailEcommercesales_ts[[response_var]].iloc[0:retailEcommercesales_ts.shape[0]-1,:]
        lag1.index = randomforest_response_var.index
        lag1 = lag1.rename(columns={response_var: 'lag1'})
        randomforest_predictors = processing.make_predictors_df(lag1, randomforest_key)

        # extra test data
        predictors_with_extra = processing.make_predictors_df(randomforest_key)
        extra_test_data = predictors_with_extra.loc[predictors_with_extra.index > randomforest_predictors.index[len(randomforest_predictors.index)-1], :]
        extra_test_data['lag1'] = randomforest_response_var.iloc[-1][0]
        randomforest_predictors = pd.concat([randomforest_predictors, extra_test_data])
        return randomforest_predictors, randomforest_response_var