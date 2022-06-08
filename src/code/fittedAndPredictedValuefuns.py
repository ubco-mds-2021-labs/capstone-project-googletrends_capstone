import pandas as pd
import numpy as np
from plotSeries import plot_df


# function to predict gdp value for test set and extra test set
def fitted_and_predicted_gdp(modelfit, pred_gdpGrowth, gdp_original, train, test, extra_test):
    # fitted gdp value for training set
    base_GDP = gdp_original['GDP'][0]
    fitted_values = modelfit.predict()
    fitted_GDP = [0]*(len(fitted_values)+1)
    fitted_GDP[0] = base_GDP
    for i, value in enumerate(fitted_values):
        fitted_GDP[i+1] = fitted_GDP[i]*(1 + value)
    fitted_GDP_df = pd.DataFrame(fitted_GDP[1:])
    fitted_GDP_df.index = train.index

    # predicted gdp value for test set
    base_GDP_test = gdp_original[gdp_original.index == train.index[-1]]['GDP'][0]
    predicted_GDP = [0]*pred_gdpGrowth.shape[0]
    actual_GDP = base_GDP_test
    if not test.empty:
        for i in range(0, test.shape[0]):
            value = pred_gdpGrowth[0][i]
            predicted_GDP[i] = actual_GDP*(1 + value)
            actual_GDP = gdp_original.loc[test.index[i]][0]
        predicted_GDP_df = pd.DataFrame(predicted_GDP)
        predicted_GDP_df.index = pred_gdpGrowth.index
        predicted_GDP_df = pd.concat([gdp_original[gdp_original.index == train.index[-1]]['GDP'], predicted_GDP_df])

        # prediction error calculation
        org = gdp_original[gdp_original.index >= predicted_GDP_df.index[0]]
        error = 0
        for i in range(0, test.shape[0]):
            error = error + (org['GDP'][i]-predicted_GDP_df[0][i])**2
        pred_error = np.sqrt(error/predicted_GDP_df.shape[0])
        #print(f"Prediction error: {pred_error}")

    # predicted gdp value for extra test set when test set is not empty
    if not extra_test.empty and not test.empty:
        base_GDP_test = gdp_original[gdp_original.index == test.index[-1]]['GDP'][0]
        actual_GDP = base_GDP_test
        for i in range(0, extra_test.shape[0]):
            value = pred_gdpGrowth.iloc[test.shape[0]+i][0]
            predicted_GDP[i] = actual_GDP*(1 + value)
            actual_GDP = predicted_GDP[i]
            predicted_GDP_df.iloc[test.shape[0]+i+1][0] = predicted_GDP[i]

    # predicted gdp value for extra test set when test set is empty
    if not extra_test.empty and test.empty:
        base_GDP_test = gdp_original[gdp_original.index == train.index[-1]]['GDP'][0]
        actual_GDP = base_GDP_test
        for i in range(0, extra_test.shape[0]):
            value = pred_gdpGrowth.iloc[i][0]
            predicted_GDP[i] = actual_GDP*(1 + value)
            actual_GDP = predicted_GDP[i]
        predicted_GDP_df = pd.DataFrame(predicted_GDP)
        predicted_GDP_df.index = pred_gdpGrowth.index
        predicted_GDP_df = pd.concat([gdp_original[gdp_original.index == train.index[-1]]['GDP'], predicted_GDP_df])
        pred_error = None


    # Plot actual and fitted GDP
    Actual_GDP = gdp_original['GDP'][1:]
    fittedandActual_GDP = pd.DataFrame({'Actual GDP': Actual_GDP,
                                        'Fitted GDP': fitted_GDP_df.squeeze(),
                                        'Predicted GDP': predicted_GDP_df.squeeze()
                                       })
    fig = plot_df(fittedandActual_GDP, width=10, height=3)
    return pred_error, fig, fittedandActual_GDP

# function to predict RTS value for test set and extra test set
def fitted_and_predicted_retail(modelfit, pred_retailGrowth, retailsales, train, test, extra_test):
    base_retail = retailsales['VALUE'][1]
    
    # calculate fitted retail sales
    X_lasso = train.loc[:, ~train.columns.isin(['GrowthRate'])]
    fitted_values = modelfit.predict(X_lasso)  # fitted growth rate
    fitted_values = pd.DataFrame(fitted_values, columns={'Fitted GrowthRate'})
    fitted_values.index = train.index
    
    fitted_retail = [0]*(len(fitted_values)+1)
    fitted_retail[0] = base_retail
    for i, value in enumerate(fitted_values['Fitted GrowthRate']):
        fitted_retail[i+1] = fitted_retail[i]*(1 + value)
    fitted_retail_df = pd.DataFrame(fitted_retail[1:])
    fitted_retail_df.index = train.index

    
    #Test
    base_retail_test = retailsales[retailsales.index == train.index[-1]]['VALUE'][0]
    predicted_retail = [0]*pred_retailGrowth.shape[0]
    actual_retail = base_retail_test
    if not test.empty:
        for i in range(0, test.shape[0]):
            value = pred_retailGrowth[0][i]
            predicted_retail[i] = actual_retail*(1 + value)
            actual_retail = retailsales.loc[test.index[i]][0]
        predicted_retail_df = pd.DataFrame(predicted_retail)
        predicted_retail_df.index = pred_retailGrowth.index
        predicted_retail_df = pd.concat([retailsales[retailsales.index == train.index[-1]]['VALUE'], predicted_retail_df])

        # prediction error calculation
        org = retailsales[retailsales.index >= predicted_retail_df.index[0]]
        error = 0
        for i in range(0, test.shape[0]):
            error = error + (org['VALUE'][i]-predicted_retail_df[0][i])**2
        pred_error = np.sqrt(error/predicted_retail_df.shape[0])
        print(f"Prediction error: {pred_error}")

    # predicted retail trade value for extra test set when test set is not empty
    if not extra_test.empty and not test.empty:
        base_retail_test = retailsales[retailsales.index == test.index[-1]]['VALUE'][0]
        actual_retail = base_retail_test
        for i in range(0, extra_test.shape[0]):
            value = pred_retailGrowth.iloc[test.shape[0]+i][0]
            predicted_retail[i] = actual_retail*(1 + value)
            actual_retail = predicted_retail[i]
            predicted_retail_df.iloc[test.shape[0]+i+1][0] = predicted_retail[i]

    # predicted retail trade value for extra test set when test set is empty
    if not extra_test.empty and test.empty:
        base_retail_test = retailsales[retailsales.index == train.index[-1]]['VALUE'][0]
        actual_retail = base_retail_test
        for i in range(0, extra_test.shape[0]):
            value = pred_retailGrowth.iloc[i][0]
            predicted_retail[i] = actual_retail*(1 + value)
            actual_retail = predicted_retail[i]
        predicted_retail_df = pd.DataFrame(predicted_retail)
        predicted_retail_df.index = pred_retailGrowth.index
        predicted_retail_df = pd.concat([retailsales[retailsales.index == train.index[-1]]['VALUE'], predicted_retail_df])
        pred_error = None


    # Plot actual and fitted retail trade
    Actual_retail = retailsales['VALUE'][1:]
    fittedandActual_retail = pd.DataFrame({'Actual Retail': Actual_retail,
                                        'Fitted Retail': fitted_retail_df.squeeze(),
                                        'Predicted Retail': predicted_retail_df.squeeze()
                                       })
    fig = plot_df(fittedandActual_retail, width=10, height=3)
    return pred_error, fig, fittedandActual_retail


def fitted_and_predicted_sales_ecommerce(modelfit, pred_EcommerceGrowth, retailEcommercesales, train, test, extra_test):
    base_sales = retailEcommercesales['Ecommerce_sales'][1]

    # calculate fitted retail sales
    X_randomforest = train.loc[:, ~train.columns.isin(['Growth_rate'])]
    fitted_values = modelfit.predict(X_randomforest)  # fitted growth rate
    fitted_values = pd.DataFrame(fitted_values, columns={'Fitted GrowthRate'})
    fitted_values.index = train.index

    fitted_sales = [0]*(len(fitted_values)+1)
    fitted_sales[0] = base_sales
    for i, value in enumerate(fitted_values['Fitted GrowthRate']):
        fitted_sales[i+1] = fitted_sales[i]*(1 + value)
    fitted_sales_df = pd.DataFrame(fitted_sales[1:])
    fitted_sales_df.index = train.index

    #Test
    base_sales_test = retailEcommercesales[retailEcommercesales.index == train.index[-1]]['Ecommerce_sales'][0]
    predicted_sales = [0]*pred_EcommerceGrowth.shape[0]
    actual_sales = base_sales_test
    if not test.empty:
        for i in range(0, test.shape[0]):
            value = pred_EcommerceGrowth[0][i]
            predicted_sales[i] = actual_sales*(1 + value)
            actual_sales = retailEcommercesales.loc[test.index[i]][0]
        predicted_sales_df = pd.DataFrame(predicted_sales)
        predicted_sales_df.index = pred_EcommerceGrowth.index
        predicted_sales_df = pd.concat([retailEcommercesales[retailEcommercesales.index == train.index[-1]]['Ecommerce_sales'], predicted_sales_df])

        # prediction error calculation
        org = retailEcommercesales[retailEcommercesales.index >= pred_EcommerceGrowth.index[0]]
        error = 0
        for i in range(0, test.shape[0]):
            error = error + (org['Ecommerce_sales'][i]-predicted_sales_df[0][i])**2
        pred_error = np.sqrt(error/predicted_sales_df.shape[0])
        print(f"Prediction error: {pred_error}")

    # predicted sales trade value for extra test set when test set is not empty
    if not extra_test.empty and not test.empty:
        base_sales_test = retailEcommercesales[retailEcommercesales.index == test.index[-1]]['Ecommerce_sales'][0]
        actual_sales = base_sales_test
        for i in range(0, extra_test.shape[0]):
            value = pred_EcommerceGrowth.iloc[test.shape[0]+i][0]
            predicted_sales[i] = actual_sales*(1 + value)
            actual_sales = predicted_sales[i]
            predicted_sales_df.iloc[test.shape[0]+i+1][0] = predicted_sales[i]

    # predicted sales trade value for extra test set when test set is empty
    if not extra_test.empty and test.empty:
        base_sales_test = retailEcommercesales[retailEcommercesales.index == train.index[-1]]['Ecommerce_sales'][0]
        actual_sales = base_sales_test
        for i in range(0, extra_test.shape[0]):
            value = pred_EcommerceGrowth.iloc[i][0]
            predicted_sales[i] = actual_sales*(1 + value)
            actual_sales = predicted_sales[i]
        predicted_sales_df = pd.DataFrame(predicted_sales)
        predicted_sales_df.index = pred_EcommerceGrowth.index
        predicted_sales_df = pd.concat([retailEcommercesales[retailEcommercesales.index == train.index[-1]]['Ecommerce_sales'], predicted_sales_df])
        pred_error = None


    # Plot actual and fitted retail trade
    Actual_sales = retailEcommercesales['Ecommerce_sales'][1:]
    fittedandActual_sales = pd.DataFrame({'Actual Retail': Actual_sales,
                                        'Fitted Retail': fitted_sales_df.squeeze(),
                                        'Predicted Retail': predicted_sales_df.squeeze()
                                       })
    fig = plot_df(fittedandActual_sales, width=10, height=3)
    return pred_error, fig, fittedandActual_sales