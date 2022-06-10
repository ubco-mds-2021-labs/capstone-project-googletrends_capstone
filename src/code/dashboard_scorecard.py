import pandas as pd
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

### Read data for all the indicators (Growth Rate)
gdp_growth_path = '../../data/storeddata/GDP_GrowthRateResults.csv'
gdp_growth = pd.read_csv(gdp_growth_path, index_col=0)
gdp_growth.index = pd.to_datetime(gdp_growth.index)
gdp_growth = gdp_growth.rename(columns={'GDP_GrowthRate': 'Actual Growth Rate'})
rts_growth_path = '../../data/storeddata/RTS_GrowthRateResults.csv'
rts_growth = pd.read_csv(rts_growth_path, index_col=0)
rts_growth.index = pd.to_datetime(rts_growth.index)
rts_growth = rts_growth.rename(columns={'GrowthRate': 'Actual Growth Rate'})
ec_growth_path = '../../data/storeddata/EComm_GrowthRateResults.csv'
ec_growth = pd.read_csv(ec_growth_path, index_col=0)
ec_growth.index = pd.to_datetime(ec_growth.index)
ec_growth = ec_growth.rename(columns={'Ecommerce_GrowthRate': 'Actual Growth Rate'})


# function to get the values
def indicator_value_scorecard(value='GDP'):
    """ function selects required data and returns the desired indicator's predicted value """
    if value == 'GDP':
        data = gdp_value
        predicted_value = data.tail()[data.tail()['Actual GDP'].isna()].head(1)['Predicted GDP'][0]

    elif value == 'RTS':
        data = rts_value
        predicted_value = data.tail()[data.tail()['Actual Retail Sales'].isna()].head(1)['Predicted Retail Sales'][0]

    elif value == 'EC':
        data = ec_value
        predicted_value = data.tail()[data.tail()['Actual Ecommerce'].isna()].head(1)['Predicted Ecommerce'][0]
    return round(predicted_value, 2)


#function to get the growth rate
def indicator_growth_rate_scorecard(value='GDP'):
    """ function selects required data and returns the desired growth rate value"""

    actual_name = "Actual Growth Rate"
    predicted_name = "Predicted Value"

    if value == 'GDP':
        data = gdp_growth 
        growth_rate = data.tail()[data.tail()[actual_name].isna()].head(1)[predicted_name][0]

    elif value == 'RTS':
        data = rts_growth
        growth_rate = data.tail()[data.tail()[actual_name].isna()].head(1)[predicted_name][0]

    elif value == 'EC':
        data = ec_growth
        growth_rate = data.tail()[data.tail()[actual_name].isna()].head(1)[predicted_name][0]
    return round(growth_rate, 4)