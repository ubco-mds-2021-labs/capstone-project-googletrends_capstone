This folder contains all the script files used for analysis and deploymnet of dashboard.

Run the three scripts in the following order to get all the results: 

1. 'script1_extractGoogleTrendsData.py' - This sscript extracts all the data and saves it in csv files
in data/storeddata folder.
2. 'script2_fitModels.py' - This script uses the data stored by 'script1_extractGoogleTrendsData.py'
and fits models to the data, and makes predictions for all the three indicators. It also stores the predicted data in 
data/storeddata dolder that is further used by script3.
3. 'script3_dashboard.py' - This script creates dashboard by uisng the data produced by script2.

The scripts used by 'script3_dashboard.py' starts with 'dashboard_*' and rest all the modules are used by first two scripts.
 

Descriptin of other important files:

1. 'Notebook_all_indicators.ipynb' - This notebook has all the code of 'script2_fitModels.py' and 'script3_dashboard.py' for all the three indicators.
2. 'FinalGDP_Notebook.ipynb' - This notebook data extraction and model fitting code for indicator GDP.
3. 'FinalRetail_Notebook.ipynb' - This notebook data extraction and model fitting code for indicator Retail Trade Sales.
4. 'FinalEcommerce_Notebook.ipynb' - This notebook data extraction and model fitting code for indicator E-commerece sales.