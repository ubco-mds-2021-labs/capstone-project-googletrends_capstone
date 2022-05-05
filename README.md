# Nowcasting Macroeconomic Indicators using Google Trends

This project aims to develop a methodology to predict macroeconomic indicators such as GDP, retail trade sales and retail e-commerce sales with real-time data source, Google Trends. The volume of queries for different keywords and categories from Google Trends API will serve as the predictors for nowcasting the desired economic factors. 

The key goals of the project are discussed below:

1) Nowcasting quarterly GDP: Our first goal is to nowcast the macroeconomic indicator GDP quarterly by using the real time Google Trends variables as predictors. The aim is to nowcast the GDP at national level and industry-wise. 

2) Nowcasting monthly retail trade sales: The retail sales data are available monthly, so our objective is to nowcast the monthly retail trade sales industry-wise using real time data.

3) Nowcasting retail e-commerce sales: The retail sales data are available monthly, so our objective is to nowcast the monthly retail e-commerce sales industry-wise using real time data.

4) Nowcast monthly GDP: As the data for GDP are available quarterly and monthly, our last objective is to nowcast monthly GDP if time permits. 



## Team Members

- Aishwarya Sharma: A data science enthusiast who loves to play with data and is always eager to explore more. 
- Harpreet Kaur: Passionate mathematician on the path of becoming a statistician.
- Jagdeep Brar: A data science student who loves cooking and painting in free time!

## Description of Topic

The information on economic indicators is crucial for policymaking and taking decision at right time but this information is usually available with a lag. So, the need for alternative data sources is of growing importance for both supplementing Statistics Canada’s data holdings and for nowcasting economic activity. The goal of this project is to develop a methodology to predict macroeconomic factors such as Gross Domestic Product (GDP), retail trade sales and retail e-commerce sales in real time by using the real time data source, Google Trends. Google Trends provides daily, weekly, and monthly reports on the volume of Google queries related to different industries which can help to understand the business cycles and provide signals about multiple aspects of the economy that can further be used to estimate the economic factors in real time. The nowcasting of economic indicators will provide more timely information for policymaking.   

## About this Project

Macroeconomic factors are the key drivers of economy, and their timely information helps in good policy making. However, this information is available with a lag, for instance, the data for the present month’s GDP is generally published in the coming month/quarter which causes delay in decision-making. To overcome this issue of delayed information gave rise to nowcasting approach. This is what this project will serve. This project will nowcast the macroeconomic factors and will use the keywords from Google Trends to predict the indicators. A dashboard will be created which will be user friendly and will be interactive in nature.

## Description of Dataset

Data set for this project are open ended and the short description about data is provided below:

1) **Gross Domestic Product (GDP) at basic prices monthly:** This dataset is a comma separated file containing the information about the monthly GDP. This file contains data from 1997 and do have some missing values, thus will require data wrangling.

2) **Gross Domestic Product (GDP) at basic prices quarterly:** This dataset is comma separated file containing the information about the GDP quarterly. This file contains data from 1997 and do have some missing values, thus will require data wrangling.

3) **Retail trade sales by province and territory:** This dataset contains information about the retail sales as per the province and territory. This data file is also comma separated and will require data wrangling.

4) **Retail trade sales by industry:** This is a comma separated data set containing the information about the retail sales trades as per the industry. Data wrangling is required in this dataset as well.

5) **Retail sales, price, and volume:** This is a comma separated data set containing monthly retail sales, price, and volume data. This data set will need some data wrangling.

6) **Retail E-commerce sales:** This is a comma separated dataset containing the information about the retail e-commerce sales. This is the data for digital sales and will require some data wrangling as well.

7) **Google Trends API:** We will be accessing Google Trends website to get real time data for the macroeconomic indicators. Different keywords, categories and subcategories will be used to extract Google Trends predictors such as Economic crisis, loans, GPS, unemployment, affordable housing, economy news, agriculture, and forestry.

Our focus will be on the data starting from 2004 as we have Google trends available from that period and this will provide us huge data for our nowcasting.



## Acknowledgements and references 


- H. Choi, H. Varian, Predicting the present with Google Trends, Economic record, 88 (2012), 2-9.
- Stock, J.H. and Watson, M.W., 2016. Dynamic factor models, factor-augmented vector autoregressions, and structural vector autoregressions in macroeconomics. In Handbook of macroeconomics (Vol. 2, pp. 415-525). Elsevier.
- Woloszko, N. (2020). Tracking activity in real time with Google Trends, OECD Economics Department Working Papers, No. 1634, OECD Publishing, Paris.
- Dauphin, M.J.F., Dybczak, M.K., Maneely, M., Sanjani, M.T., Suphaphiphat, M.N., Wang, Y. and Zhang, H., 2022. Nowcasting GDP-A Scalable Approach Using DFM, Machine Learning and Novel Data, Applied to European Economies. International Monetary Fund.
- Richardson, A., van Florenstein Mulder, T. and Vehbi, T., 2021. Nowcasting GDP using machine-learning algorithms: A real-time assessment. International Journal of Forecasting, 37(2), pp.941-948.

