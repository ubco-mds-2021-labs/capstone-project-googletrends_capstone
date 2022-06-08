from statsmodels.tsa.stattools import kpss, adfuller
import statsmodels.api as sm
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

class stationarityTest():

    def adf_test(timeseries):
        #print("Results of Dickey-Fuller Test:")
        dftest = adfuller(timeseries, autolag="AIC")
        dfoutput = pd.Series(
            dftest[0:4],
            index=[
                "Test Statistic",
                "p-value",
                "#Lags Used",
                "Number of Observations Used",
            ],
        )
        for key, value in dftest[4].items():
            dfoutput["Critical Value (%s)" % key] = value
        #print(dfoutput)
        if dftest[1] < 0.05:
            return f"Series is stationary"
        else:
            return f"Series is not stationary"


    def kpss_test(timeseries):
        #print("Results of KPSS Test:")
        kpsstest = kpss(timeseries, regression="c", nlags="auto")
        kpss_output = pd.Series(
            kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
        )
        for key, value in kpsstest[3].items():
            kpss_output["Critical Value (%s)" % key] = value
        #print(kpss_output)
        if kpsstest[1] > 0.05:
            return f"Series is stationary"
        else:
            return f"Series is not stationary"

class check_stationaritytest(stationarityTest):
    def check_stationarity(dataframe):
        for i in range(0,dataframe.shape[1]):
            timeseries = dataframe.iloc[:,i]
            adf_result = stationarityTest.adf_test(timeseries)
            kpss_result = stationarityTest.kpss_test(timeseries)
            if (adf_result == "Series is stationary") and (kpss_result == "Series is stationary"):
                pass
            elif (adf_result == "Series is not stationary") and (kpss_result == "Series is not stationary"):
                print(f"Series {dataframe.columns[i]} is not stationary")
            elif (adf_result == "Series is stationary") and (kpss_result == "Series is not stationary"):
                print(f"Series {dataframe.columns[i]} is not stationary, differencing can be used to make it stationary")
            elif (adf_result == "Series is not stationary") and (kpss_result == "Series is stationary"):
                print(f"Series {dataframe.columns[i]} is trend stationary, trend needs to be removed")
        print("All other series are stationary")