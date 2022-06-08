import pandas as pd
from scipy.stats import pearsonr


# selection of predictors frequency based
def predictor_selection(dataframe, year="2005-01-01"):
    temp_data = dataframe.copy()
    q_index = dataframe[(dataframe.index > year)].max()
    for i, qidx in enumerate(q_index):
        if qidx == 100:
            continue
        else:
            temp_data = temp_data.drop(columns=[q_index.index[i]])
    return temp_data


# selection of variables correlation based
def select_variables_with_correlation(response_gdpts, predictors_dataframe, req_corr=0.6):
    """ dataframe is 'categoryts' here"""
    predictors_dataframe.index = pd.to_datetime(predictors_dataframe.index)
    cols = list()
    data = pd.merge(response_gdpts, predictors_dataframe, left_index=True, right_index=True)

    for i in range(0, data.iloc[:, 2:].shape[1]):
        corr, _ = pearsonr(data['GDP'], data.iloc[:, i+2])
        if abs(corr) > req_corr:
            cols.append(data.columns[i+2])
    return predictors_dataframe[cols]