# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import time

from statistics import mean, stdev
from pytrends.request import TrendReq
from urllib3.exceptions import MaxRetryError

from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.api as sm

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import warnings

# our modules
from plotSeries import *
from checkStationarity import *
from GoogleTrendsData import *
from makeDataQuarterly import *
from makeSeriesStationary import *
from predictorsSelection import *
from dataPreProcessing import *
from tsModels import *
from rollingPredictionfuns import *
from fittedAndPredictedValuefuns import *
from bootstrapfuns import *



################################################################################
##########                     Read  Data                      #################
################################################################################

################################## GDP Data ###################################################
# Read statCan data for GDP
warnings.filterwarnings("ignore")
gdp_path = '../../data/expenditure/expenditure_gdp_new.csv'
gdp = pd.read_csv(gdp_path)
gdp['REF_DATE'] = pd.to_datetime(gdp['REF_DATE'])

# filter data
gdp_subset = gdp[(gdp['REF_DATE'] >= '2004-01-01') &
                (gdp['Prices'] == 'Chained (2012) dollars') & 
                (gdp['Estimates'] == 'Gross domestic product at market prices') &
                 (gdp['UOM'] == 'Dollars')]
gdpts = gdp_subset[['REF_DATE', 'VALUE']]

# rename columns
gdpts = gdpts.rename(columns = {'REF_DATE': 'Date', 'VALUE': 'GDP'})
gdpts.index = gdpts['Date']
gdpts = gdpts.drop(columns = ['Date'])

# create copy of original data to use later
gdp_original = gdpts.copy()

# calculate and add growth rate to the dataframe
gdpts['GDP_GrowthRate'] = gdpts['GDP'].pct_change()
gdpts = gdpts.dropna()

# Read trends data for GDP
categoryts = pd.read_csv('../../data/storeddata/gdp_category_ts.csv', index_col=0)


################################## Retail Trades Data ###################################################
# Reading file
retailsales=pd.read_csv('../../data/retailsalesbyIndustry/retailSalesbyIndustry.csv')
# Renaming columns as required
retailsales.rename(columns = {'REF_DATE':'date', 
                                            'GEO':'LOCATION',
                                            'North American Industry Classification System (NAICS)':'INDUSTRY',
                                            'Adjustments':'ADJUSTMENTS'
                                           },inplace = True)

# Filtering columns as needed and extracting required columns
retailsales_filtered=retailsales[(retailsales['LOCATION'] == 'Canada') & 
                 (retailsales['INDUSTRY'] == 'Retail trade [44-45]')&
                 (retailsales['ADJUSTMENTS'] == 'Seasonally adjusted')&
                 (retailsales['date'] >= '2004-01')]
retailsales_final = retailsales_filtered[['date', 'VALUE']].copy()

#Changing data type of date
retailsales_final['date'] =  pd.to_datetime(retailsales_final['date'])
retailsales_final = retailsales_final.set_index('date')
retailsales_initial = retailsales_final.copy()

# calculate and add growth rate to the dataframe
retailsales_final['GrowthRate']=retailsales_final['VALUE'].pct_change()
retailsales_final = retailsales_final.dropna()

# Read Trends data for retial trade sales
corrcat = pd.read_csv('../../data/storeddata/FinalRetailData.csv')
corrcat = corrcat.set_index('date')
corrquery = pd.read_csv('../../data/storeddata/keywords_query_nonstationary.csv')
corrquery = corrquery.set_index('date')

################################## E-Commerce Data ###################################################
# Reading file
data = pd.read_csv('../../data/retailEcommercesales/retailEcommerceSales.csv',sep=',')
# data filter
retailEcommercesales = data[~data["Sales"].str.contains('unadjusted')]
retailEcommercesales = retailEcommercesales.filter(['REF_DATE','VALUE'])
# rename columns
retailEcommercesales = retailEcommercesales.rename(columns = {'REF_DATE': 'Date', 'VALUE': 'Ecommerce_sales'})
retailEcommercesales_ts = retailEcommercesales.copy()
#Changing data type of date
retailEcommercesales=retailEcommercesales.set_index(['Date'])
retailEcommercesales.index = pd.to_datetime(retailEcommercesales.index)
retailEcommercesales_ts = retailEcommercesales_ts.set_index('Date')
retailEcommercesales_ts.index = pd.to_datetime(retailEcommercesales_ts.index)
# calculate and add growth rate to the dataframe
retailEcommercesales_ts['Growth_rate'] = retailEcommercesales_ts.pct_change()
retailEcommercesales_ts = retailEcommercesales_ts.dropna() # removing NA

# Read and process trends data
ecommerce_keyword_ts = pd.read_csv('../../data/storeddata/EcommerceKeywordTimeSeries.csv')
ecommerce_keyword_ts.rename(columns = {'date':'Date'}, inplace = True)
ecommerce_keyword_ts = ecommerce_keyword_ts.set_index(['Date'])
ecommerce_keyword_ts.index = pd.to_datetime(ecommerce_keyword_ts.index)
ecommerce_keyword_ts = ecommerce_keyword_ts.dropna()