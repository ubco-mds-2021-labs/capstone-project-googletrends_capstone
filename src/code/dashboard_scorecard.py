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

def indicator_value_scorecard(value='GDP', from_year=2004, end_year = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')).year):
    """ function selects required data and returns the desired indicator's value plot for provided year range"""
    if value == 'GDP':
        data = gdp_value
        actual_name = "Actual GDP"
        predicted_name = "Predicted GDP"
        
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        predicted_value = data.tail()[data.tail()['Actual GDP'].isna()].head(1)['Predicted GDP'][0]

    elif value == 'RTS':
        data = rts_value
        actual_name = "Actual Retail Sales"
        predicted_name = "Predicted Retail Sales"
       
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        predicted_value = data.tail()[data.tail()['Actual Retail Sales'].isna()].head(1)['Predicted Retail Sales'][0]

    elif value == 'EC':
        data = ec_value
        actual_name = "Actual Ecommerce"
        predicted_name = "Predicted Ecommerce"
            
        data=data[(data.index.year >= from_year) & (data.index.year <= end_year)]

        predicted_value = data.tail()[data.tail()['Actual Ecommerce'].isna()].head(1)['Predicted Ecommerce'][0]
    return predicted_value