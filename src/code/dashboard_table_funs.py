import pandas as pd
import math


IndicatorValues_gdp = pd.read_csv('../../data/storeddata/GDP_ValueResults.csv')
IndicatorGrowth_gdp = pd.read_csv('../../data/storeddata/GDP_GrowthRateResults.csv')
IndicatorValues_rts = pd.read_csv('../../data/storeddata/RTS_ValueResults.csv')
IndicatorGrowth_rts = pd.read_csv('../../data/storeddata/RTS_GrowthRateREsults.csv')
IndicatorValues_ec = pd.read_csv('../../data/storeddata/Ecomm_ValueResults.csv')
IndicatorGrowth_ec = pd.read_csv('../../data/storeddata/Ecomm_GrowthRateResults.csv')


def Count_predicted_growth_rates(indicator):
    """ returns the number of predicted growth rates to color those rows"""

    if indicator == "GDP":
        IndicatorGrowth = IndicatorGrowth_gdp
    if indicator == "RTS":
        IndicatorGrowth = IndicatorGrowth_rts
    if indicator == "EC":
        IndicatorGrowth = IndicatorGrowth_ec
    return 5-IndicatorGrowth.iloc[:,1].isna().sum()
    

def ValueTable(indicator):
    """ The dashboard`s Value and Prediction Interval table"""

    if indicator == "GDP":
        IndicatorValues = IndicatorValues_gdp
    if indicator == "RTS":
        IndicatorValues = IndicatorValues_rts
    if indicator == "EC":
        IndicatorValues = IndicatorValues_ec

    IndicatorValues = IndicatorValues.tail(5)        
    IndicatorValues_Table = IndicatorValues.iloc[:,[0,1,3,4,5,6]]
    IndicatorValues_Table.rename(columns={list(IndicatorValues_Table)[0]:'Date'}, inplace=True)
    IndicatorValues_Table.rename(columns={list(IndicatorValues_Table)[2]:'Predicted Value'}, inplace=True)
    IndicatorValues_Table.rename(columns={list(IndicatorValues_Table)[3]:'Prediction Interval (2.5%)'}, inplace=True)
    IndicatorValues_Table.rename(columns={list(IndicatorValues_Table)[4]:'Prediction Interval (97.5%)'}, inplace=True)
    #IndicatorValues_Table.reset_index(inplace=True)
    IndicatorValues_Table.iloc[:, 2:] = round(IndicatorValues_Table.iloc[:,2:], 2)
    for i in range(1,6):
        IndicatorValues_Table.iloc[:,i] = IndicatorValues_Table.iloc[:,i].map('{:,}'.format)

    #IndicatorValues_Table.iloc[:,1] = IndicatorValues_Table.iloc[:,1].fillna(0)

    months_dict = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8':'Aug', 
                    '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    
    IndicatorValues_Table = IndicatorValues_Table.reset_index()
    temp_df = IndicatorValues_Table.copy()
    temp_df.iloc[:,1] = pd.to_datetime(temp_df.iloc[:,1])
    for i in range(0, IndicatorValues_Table.shape[0]):
        month_temp = str(temp_df.iloc[:,1][i].month)
        year_temp = str(temp_df.iloc[:,1][i].year)
        IndicatorValues_Table.iloc[:,1][i] = months_dict[month_temp]+"-"+year_temp
    IndicatorValues_Table.iloc[:,2] = IndicatorValues_Table.iloc[:,2].replace('nan', '-')
    return IndicatorValues_Table.iloc[:,1:]


###############################################################################################
def GrowthValueTable(indicator):
    """ The dashboard`s Growth and Value table"""

    if indicator == "GDP":
        IndicatorValues = IndicatorValues_gdp
        IndicatorGrowth = IndicatorGrowth_gdp
        IndicatorGrowth.rename(columns={'GDP_GrowthRate': 'Growth Rate'}, inplace=True)
        IndicatorValues.rename(columns={'Actual GDP': 'GDP Value'}, inplace=True)
    if indicator == "RTS":
        IndicatorValues = IndicatorValues_rts
        IndicatorGrowth = IndicatorGrowth_rts
        IndicatorGrowth.rename(columns={'GrowthRate': 'Growth Rate'}, inplace=True)
        IndicatorValues.rename(columns={'Actual Retail Sales': 'RTS Value'}, inplace=True)
    if indicator == "EC":
        IndicatorValues = IndicatorValues_ec
        IndicatorGrowth = IndicatorGrowth_ec
        IndicatorGrowth.rename(columns={'Ecommerce_GrowthRate': 'Growth Rate'}, inplace=True)
        IndicatorValues.rename(columns={'Actual Ecommerce': 'EC Sales Value'}, inplace=True)

    GrowthValue_DF = pd.merge(IndicatorGrowth,IndicatorValues, left_index=True, right_index=True,how="left")
    GrowthRateResults_Table = GrowthValue_DF.tail(5)
    GrowthRateResults_Table = GrowthRateResults_Table.iloc[:,[0,1,3,8,10]]

    for i in range(len(GrowthRateResults_Table)):   
        if math.isnan(GrowthRateResults_Table.iloc[i,1]):
            GrowthRateResults_Table.iloc[i,1] = GrowthRateResults_Table.iloc[i,2]
        if math.isnan(GrowthRateResults_Table.iloc[i,3]):
            GrowthRateResults_Table.iloc[i,3] = GrowthRateResults_Table.iloc[i,4]
        
    GrowthRateResults_Table = GrowthRateResults_Table.iloc[:,[0,1,3]]
    GrowthRateResults_Table.rename(columns={list(GrowthRateResults_Table)[0]:'Date'}, inplace=True)
    GrowthRateResults_Table = round(GrowthRateResults_Table,4)
    GrowthRateResults_Table.iloc[:, 2] = round(GrowthRateResults_Table.iloc[:,2], 2)
    GrowthRateResults_Table.iloc[:,2] = GrowthRateResults_Table.iloc[:,2].map('{:,}'.format)
    #GrowthRateResults_Table.reset_index(inplace=True)
    
    months_dict = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8':'Aug', 
                    '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    
    GrowthRateResults_Table = GrowthRateResults_Table.reset_index()
    temp_df = GrowthRateResults_Table.copy()
    temp_df.iloc[:,1] = pd.to_datetime(temp_df.iloc[:,1])
    for i in range(0, GrowthRateResults_Table.shape[0]):
        month_temp = str(temp_df.iloc[:,1][i].month)
        year_temp = str(temp_df.iloc[:,1][i].year)
        GrowthRateResults_Table.iloc[:,1][i] = months_dict[month_temp]+"-"+year_temp
        
    return GrowthRateResults_Table.iloc[:,1:]

