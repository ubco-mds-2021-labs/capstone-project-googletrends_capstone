import pandas as pd


def get_gdp_data_quarterly(dataframe, match='0'):
    """ provides quarterly data of gdp predictors when monthly data is passed 
    input arguments: 
    dataframe: monthly data of google trends
    match: can take values '0', '-1', '-2', '-01', '-12', '-02', '-012'
           if match = 0 then data of months 1, 4, 7, 10 is returned that is same month when GDP is published
           if match = -1 then data (Google Trends) of one previous month 12, 3, 6, 9 are returned 
           if match = -2 then data (Google Trends) of one previous month 11, 2, 5, 8 are returned
           if match = -01 then data of same and previous month data is returned
           if match = -12 then data of two previous months is returned
           if match = -012 then data of all three months is returned"""
    if match not in ['0', '-1', '-2', '-01', '-12', '-012', '-02']:
        raise ValueError("Incorrect match value is passed !!")

    try:
        dataframe.index = pd.to_datetime(dataframe.index)

        same_month_data = dataframe[(dataframe.index.month == 4) |
                                    (dataframe.index.month == 7) |
                                    (dataframe.index.month == 10) |
                                    (dataframe.index.month == 1)]

        one_month_back_data = dataframe[(dataframe.index.month == 3) |
                                        (dataframe.index.month == 6) |
                                        (dataframe.index.month == 9) |
                                        (dataframe.index.month == 12)]
        one_month_back_data.index = one_month_back_data.index + pd.DateOffset(months=1)

        two_months_back_data = dataframe[(dataframe.index.month == 2) |
                                        (dataframe.index.month == 5) |
                                        (dataframe.index.month == 8) |
                                        (dataframe.index.month == 11)]
        two_months_back_data.index = two_months_back_data.index + pd.DateOffset(months=2)

        if str(match) == '0':
            return same_month_data
        if str(match) == '-1':
            return one_month_back_data
        if str(match) == '-2':
            return two_months_back_data
        if str(match) == '-01':
            return pd.merge(same_month_data, one_month_back_data, left_index=True, right_index=True)
        if str(match) == '-12':
            return pd.merge(one_month_back_data, two_months_back_data, left_index=True, right_index=True)
        if str(match) == '-012':
            temp = pd.merge(same_month_data, one_month_back_data, left_index=True, right_index=True)
            return pd.merge(temp, two_months_back_data, left_index=True, right_index=True)
        if str(match) == '-02':
            return pd.merge(same_month_data, two_months_back_data, left_index=True, right_index=True)
    except:
        print("Incorrect dataframe is passed !!")