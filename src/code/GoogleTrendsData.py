from pytrends.request import TrendReq
import time
from datetime import datetime


# create instance 
pytrends = TrendReq(hl='en-US', backoff_factor=0.1, timeout=(10,25))



def get_trends_GDP(keyword=[''], category='0', related_queries=0, related_topics=0):
    """ function to get the google trend for desired keyword and category"""
    kw_list = keyword
    cat = category
    timeframe = '2004-01-01 '+datetime.today().strftime('%Y-%m-%d')
    geo = 'CA'
    gprop = ''

    try:
        pytrends.build_payload(kw_list, cat, timeframe, geo, gprop)
        # get time series
        data = pytrends.interest_over_time()
    except:
        print(f"Category {cat} does not exist or keyword {kw_list[0]} has no time series")
        return [''], [''], ['']

    # get related queries
    try:
        if related_queries > 0:
            queries = pytrends.related_queries()
            if len(kw_list) == 0:
                queries_lst = list(queries['']['top']['query'].values[0:related_queries])
            else:
                queries_lst = list(queries[kw_list[0]]['top']['query'].values[0:related_queries])
        else:
            queries_lst = ['']
    except:
        queries_lst = ['']

    # get related topics
    try:
        if related_topics > 0:
            topics = pytrends.related_topics()
            if len(kw_list) == 0:
                topics_lst = list(topics['']['top']['topic_title'].values[0:related_topics])
            else:
                topics_lst = list(topics[kw_list[0]]['top']['topic_title'].values[0:related_topics])
        else:
            topics_lst = ['']
    except:
        topics_lst = ['']
    return data, queries_lst, topics_lst


# get timeseries dataframe of related queries and topics (top 2) of different selected categories
def get_trends_for_dict_GDP(dict, no_related_words):
    """Returns data of passed on keywords or topics dictionary"""
    i = 0
    for key, value in dict.items():
        if no_related_words > len(value):
            print("Number of related words should not exceed {len(value)}.")
        else:
            category = key
            temp_lst = value[0:no_related_words]  # how may related words we want data for
            kw_lst = list(set(temp_lst))                # removes the repeated keywords
            for keyword in kw_lst:
                data, _, _ = get_trends_GDP(keyword=[keyword], category=category)

                # Code to append data for different keywords in data frame
                colname = category+"_"+keyword
                if i == 0:
                    data.rename(columns={keyword: colname}, inplace=True)
                    df = data.drop(columns=['isPartial'])
                else:
                    data.rename(columns={keyword: colname}, inplace=True)
                    data = data.drop(columns=['isPartial'])
                    df = df.join(data)
                i = i+1
                time.sleep(5)
    return df




#For Retail Trade Sales
# For categories
def get_trend_RTS(keyword=[''], category='0'):
    """ Function for getting trends for selected keywords
        
        arguments: 
        
        Keywords: data type is string: stores list of keywords
        category: data type is string: stores the code for category
        
        returns: google trend data, related queries and related topics as a data frame  
    """
    
    kw_list=keyword
    cat=category
    timeframe='2004-01-01 '+datetime.today().strftime('%Y-%m-%d')
    geo ='CA'
    gprop =''
    
    pytrends.build_payload(kw_list, cat, timeframe, geo, gprop)
    data = pytrends.interest_over_time()
    queries = pytrends.related_queries()
    topics = pytrends.related_topics()
    return data, queries, topics


# For Keywords
def get_trends_for_dict_RTS(dict):
    i = 0
    for key, value in dict.items():
        category = key
        kw_lst = set(value)  # removes the repeated keywords
        for keyword in kw_lst:
            data, _, _ = get_trend_RTS(keyword=[keyword], category=category)

            # Code to append data for different keywords in data frame
            colname = category+"_"+keyword
            if len(data)==0:
                continue
            else:
                if i == 0:
                    data.rename(columns={keyword: colname}, inplace=True)
                    df = data.drop(columns=['isPartial'])
                else:
                    data.rename(columns={keyword: colname}, inplace=True)
                    data = data.drop(columns=['isPartial'])
                    df = df.join(data)
            i = i+1       
            
    return df

#For E-commerce

def ecommerce_trend(keywords = [''],category = '340'):  #subcat - 280
    
    """ 
    Function for getting trends for selected keywords
        
        arguments: 
        
            Keywords: List of String ser
            category: String: stores the code for category
        
        returns: Related queries and related topics from google trend as a data frame
    """
    kw_list = keywords
    cat = category
    timeframe = '2004-01-01 '+datetime.today().strftime('%Y-%m-%d')
    geo = 'CA'
    
    pytrends.build_payload(kw_list, cat, timeframe, geo, gprop = '')
    data = pytrends.interest_over_time()
    queries = pytrends.related_queries()
    topics = pytrends.related_topics()
    
    return data, queries, topics