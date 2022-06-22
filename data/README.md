## All Data Files

This directory includes any data files that are used for accomplishing the project work.

### Subfolders

- **expenditure:** Includes Statistics Canada website historical data in a comma separated format. The data contains information about the Gross Domestic Product (GDP) quarterly. 

- **keywords_data:** Includes separate csv files for each of the three indicators. The files contain list of all the keywords/subcategories which have been used to extract the Google Trend time series.

- **retailEcommercesales:** Includes Statistics Canada website historical data in a comma separated format. The data contains information about the monthly E-Commerce (EC) sales.

- **retailsalesbyIndustry:** Includes Statistics Canada website historical data in a comma separated format. The data contains information about the monthly Retail Trade Sales (RTS) as per the industry. 

- **storeddata:** The directory includes separate files for each of the indicator. The csv files contains the growth rate and the actual values nowcasted from the model fitting. Also, the prediction error, prediction interval obtained from the selected model has been added.



To reproduce the results, three csv files need to be replaced with the new csv files (Statistics Canada's data for three indicators). 
Please download the below mentioned csv files as 'entire table in csv format' (this option is available while downloading the file). 
The details of these files are mentioned below:
 
1. **'data/expenditure/expenditure_gdp_new.csv'**: After every quarter when new GDP is released then this file should be 
replaced by the new csv file that contains the expenditure based GDP (Table number: 36100104). Please rename the new file as 'expenditure_gdp_new.csv'.

2. **'data/retailsalesbyIndustry/retailSalesbyIndustry.csv'**: After every month when new Retail Sales are 
released then this file should be replaced by the new csv file that contains the 
newly released sales (Table number: 20100008). Please rename the new file as 
'retailSalesbyIndustry.csv'.

2. **'data/retailEcommercesales/retailEcommerceSales.csv'**: After every month when new E-Commerce Sales are 
released then this file should be replaced by the new csv file that contains the 
newly released E-Commerce sales (Table number: 20100072). Please rename the new file as 
'retailEcommerceSales.csv'.
