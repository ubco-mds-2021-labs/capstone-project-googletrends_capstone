# imports
import pandas as pd
import numpy as np
import time
import warnings

from pytrends.request import TrendReq

# our modules
from GoogleTrendsData import *


##################################### GDP ###########################################

# get caegories and keywords from csv file for GDP
key_path = '../../data/keywords_data/GDP.csv'
key_data = pd.read_csv(key_path)
cat_lst = key_data['CatNo'].unique()                    # list of categories
keywords_lst = key_data['Keywords'].dropna()            # list of selected keywords
keyCat_lst = key_data['keywordCatNo'].astype('Int64').dropna()   # list of categories corresponding to keywords

# get dataframe of timeseries for categories (GDP)

cat_queries_dict = {}
cat_topics_dict = {}

# get time series and related queries and topics of categories
for i, category in enumerate(cat_lst):
    category = str(category)
    data, queries, topics = get_trends_GDP(category=category, related_queries=2, related_topics=2)
    cat_queries_dict[category] = queries
    cat_topics_dict[category] = topics

    # Code to append data for different columns in data frame
    if i == 0:
        data.rename(columns={'': category}, inplace=True)
        categoryts = data.drop(columns=['isPartial'])
    else:
        data.rename(columns={'': category}, inplace=True)
        data = data.drop(columns=['isPartial'])
        categoryts = categoryts.join(data)


# write data to csv
categoryts.to_csv('../../data/storeddata/gdp_category_ts.csv')


##################################### Retail Trade Sales ###########################################


# Reading file for Categories
retailcat=pd.read_csv('../../data/keywords_data/RETAIL_SALES.csv')
retailcatdat = retailcat[['CatNo']].copy()

# get dataframe of timeseries for categories (RTS)
keywordsDictQuery = dict() #Dictionary for queries
keywordsDictTopic = dict() #Dictionary for topic

for index, row in retailcatdat.iterrows():
    
    #Calling function
    data, queries, topics = get_trend_RTS(keyword=[''],category=str(row['CatNo']))
    
    
    #Code to append data for different columns in data frame
    
    if index==0:
        FinalData, queries, topics=get_trend_RTS(keyword=[''],category=str(row['CatNo']))
        FinalData.rename(columns = {'':str(row['CatNo'])}, inplace = True)
        FinalData=FinalData.drop(columns=['isPartial'])
    else:
        data, queries, topics=get_trend_RTS(keyword=[''],category=str(row['CatNo']))
        data.rename(columns = {'':str(row['CatNo'])}, inplace = True)
        data=data.drop(columns=['isPartial'])
        data = data[str(row['CatNo'])]
        FinalData = FinalData.join(data)
    
    #Code to store queries in a dictionary
    queries = queries['']['top']
    top5_query = pd.DataFrame(queries['query'].copy().head(5))
    top5_query = top5_query['query'].values.tolist()  
    keywordsDictQuery[str(row['CatNo'])] = top5_query
    
    #Code to store topics in a dictionary
    topics = topics['']['top']
    top5_topic = pd.DataFrame(topics['topic_title'].copy().head(5))
    top5_topic = top5_topic['topic_title'].values.tolist()
    keywordsDictTopic[str(row['CatNo'])] = top5_topic
    
# For queries
keywords_query = get_trends_for_dict_RTS(keywordsDictQuery)

# write data to csv
FinalData.to_csv('../../data/storeddata/FinalRetailData.csv')
keywords_query.to_csv('../../data/storeddata/keywords_query_nonstationary.csv')


##################################### E-Commerce Sales ###########################################

# Reading keywords
keywords_csv = pd.read_csv('../../data/keywords_data/EECOMMERCE.csv')

# extracting timeseries dataframe
for index, row in keywords_csv.iterrows():
    #calling Pytrends
    data, queries, topics=ecommerce_trend(keywords=[str(row['Keyword'])],category=str(row['SubcatNo']))
    
    if index==0:
        FinalData_e, queries, topics=ecommerce_trend(keywords=[str(row['Keyword'])],category=str(row['SubcatNo']))
        FinalData_e.rename(columns = {'':str(row['Keyword'])}, inplace = True)    #column name for frame
        FinalData_e=FinalData_e.drop(columns=['isPartial'])   #remove column
    else:
        data, queries, topics=ecommerce_trend(keywords=[str(row['Keyword'])],category=str(row['SubcatNo']))
        data.rename(columns = {'':str(row['Keyword'])}, inplace = True)
        data=data.drop(columns=['isPartial'])
        data = data[str(row['Keyword'])]
        FinalData_e = FinalData_e.join(data)

# write data to csv
FinalData.to_csv('../../data/storeddata/EcommerceKeywordTimeSeries.csv')
