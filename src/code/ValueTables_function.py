import pandas as pd
import math

def ValueTable(indicator):
    """ The dashboard`s Value and Prediction Interval table"""

    if indicator == "GDP":
        IndicatorValues = pd.read_csv('../../data/storeddata/GDP_ValueResults.csv')

    if indicator == "Retailsales":
        IndicatorValues = pd.read_csv('../../data/storeddata/RTS_ValueResults.csv')

    if indicator == "Ecommerce":
        IndicatorValues = pd.read_csv('../../data/storeddata/Ecomm_ValueResults.csv')


    IndicatorValues = IndicatorValues.tail(5)

    for i in range(len(IndicatorValues)):
        
        if math.isnan(IndicatorValues.iloc[i,1]):
            IndicatorValues.iloc[i,1] = IndicatorValues.iloc[i,3]
        
    IndicatorValues_Table = IndicatorValues.iloc[:,[0,1,4,5,6]]
    IndicatorValues_Table.rename(columns={list(IndicatorValues_Table)[0]:'Date'}, inplace=True)
    IndicatorValues_Table.rename(columns={list(IndicatorValues_Table)[2]:'Prediction Interval (2.5%)'}, inplace=True)
    IndicatorValues_Table.rename(columns={list(IndicatorValues_Table)[3]:'Prediction Interval (97.5%)'}, inplace=True)
    IndicatorValues_Table.reset_index(inplace=True)
    return IndicatorValues_Table

