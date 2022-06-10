import pandas as pd
import math

def GrowthValueTable(indicator):
    """ The dashboard`s Growth and Value table"""

    if indicator == "GDP":
        IndicatorValues = pd.read_csv('../../data/storeddata/GDP_ValueResults.csv')
        IndicatorGrowth = pd.read_csv('../../data/storeddata/GDP__GrowthRateResults.csv')
    
    if indicator == "Retailsales":
        IndicatorValues = pd.read_csv('../../data/storeddata/RTS_ValueResults.csv')
        IndicatorGrowth = pd.read_csv('../../data/storeddata/RTS_GrowthRateREsults.csv')

    if indicator == "Ecommerce":
        IndicatorValues = pd.read_csv('../../data/storeddata/Ecomm_ValueResults.csv')
        IndicatorGrowth = pd.read_csv('../../data/storeddata/Ecomm_GrowthRateResults.csv')

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
    GrowthRateResults_Table.reset_index(inplace=True)
    return GrowthRateResults_Table
