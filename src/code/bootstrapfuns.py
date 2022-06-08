import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arch.bootstrap import optimal_block_length, CircularBlockBootstrap
from numpy.random import RandomState


# function to get the bootstrap samples

def get_bootstrap_samples(train_data, n_sample=100, block_size = 10, rs=None):
    """ get circular and overlapping bootstrap samples """

    #block_size = int(optimal_block_length(train_data).mean()[1])
    #print("Block size: ", block_size)
    bs = CircularBlockBootstrap(block_size, train_data, random_state=rs)
    bs_data_lst = list()

    # create list of bootstrap samples
    for data in bs.bootstrap(n_sample):
        data[0][0].index = train_data.index
        bs_data_lst.append(data[0][0])
    return bs_data_lst

#################################################### GDP FUNCTIONS####################################################

# function to plot prediction band for growth rate and also returns prediction band data
def growth_rate_plot_and_data_bs(predicted_growth_df=None,
                              lower_q = 0.025,
                              upper_q = 0.975,
                              modelfit= None, 
                              gdpts = None, 
                              train = None,
                              pred_gdpGrowth = None):

    pred_growth_rate_data = pd.DataFrame(columns=['Predicted GDP Growth Rate',
                                                  'Prediction interval (2.5%)',
                                                  'Prediction interval (97.5%)',
                                                  'Mean (Prediction interval)'])
    # calcualte quantiles
    quantiles = predicted_growth_df.quantile(q=[0.025, 0.975], axis=1, interpolation='linear')
    growth_quantiles = np.transpose(quantiles)

    pred_growth_rate_data['Predicted GDP Growth Rate'] = pred_gdpGrowth
    pred_growth_rate_data['Prediction interval (2.5%)'] = growth_quantiles[lower_q]
    pred_growth_rate_data['Prediction interval (97.5%)'] = growth_quantiles[upper_q]
    pred_growth_rate_data['Mean (Prediction interval)'] = predicted_growth_df.mean(axis=1)

    # organise data for plot
    pred_gdpGrowth_for_plot = pd.concat([train['GDP_GrowthRate'].tail(1), pred_gdpGrowth])
    fitted_values = pd.DataFrame({'GDP_GrowthRate': gdpts['GDP_GrowthRate'],
                                  'Fitted Value': modelfit.predict(),
                                  'Predicted Value': pred_gdpGrowth_for_plot.squeeze()})

    # plot
    fitted_values.index = pd.to_datetime(fitted_values.index)
    fig = plt.figure(figsize=(12, 4), dpi=100)
    plt.plot(fitted_values, marker='o', markersize=4)
    plt.plot(predicted_growth_df.mean(axis=1), color='green', linestyle='--')
    plt.fill_between(growth_quantiles.index, growth_quantiles[lower_q], growth_quantiles[upper_q], alpha = 0.2, color = 'green')
    plt.gca().set(title="", xlabel="", ylabel="")
    plt.close()

    # combine all fitted and predicted data
    growth_quantiles['Mean (Prediction invertal)'] = predicted_growth_df.mean(axis=1)
    all_data = fitted_values.join(growth_quantiles)
    return fig, all_data


def growth_rate_plot_and_data_bs_ecommerce(predicted_growth_df=None,
                              lower_q = 0.025,
                              upper_q = 0.975,
                              modelfit= None, 
                              retailEcommercesales_ts = None, 
                              train = None,
                              pred_gdpGrowth = None,fitted_growthrate=None):

    pred_growth_rate_data = pd.DataFrame(columns=['Predicted E-commerce Growth Rate',
                                                  'Prediction interval (2.5%)',
                                                  'Prediction interval (97.5%)',
                                                  'Mean (Prediction interval)'])
    # calcualte quantiles
    quantiles = predicted_growth_df.quantile(q=[0.025, 0.975], axis=1, interpolation='linear')
    growth_quantiles = np.transpose(quantiles)

    pred_growth_rate_data['Predicted E-commerce Growth Rate'] = pred_gdpGrowth
    pred_growth_rate_data['Prediction interval (2.5%)'] = growth_quantiles[lower_q]
    pred_growth_rate_data['Prediction interval (97.5%)'] = growth_quantiles[upper_q]
    pred_growth_rate_data['Mean (Prediction interval)'] = predicted_growth_df.mean(axis=1)

    # organise data for plot
    pred_gdpGrowth_for_plot = pd.concat([train['Growth_rate'].tail(1), pred_gdpGrowth])
    fitted_values = pd.DataFrame({'Ecommerce_GrowthRate': retailEcommercesales_ts['Growth_rate'],
                                  'Fitted Value': fitted_growthrate.squeeze(),
                                  'Predicted Value': pred_gdpGrowth_for_plot.squeeze()})

    # plot
    fitted_values.index = pd.to_datetime(fitted_values.index)
    fig = plt.figure(figsize=(12, 4), dpi=100)
    plt.plot(fitted_values, marker='o', markersize=4)
    plt.plot(predicted_growth_df.mean(axis=1), color='green', linestyle='--')
    plt.fill_between(growth_quantiles.index, growth_quantiles[lower_q], growth_quantiles[upper_q], alpha = 0.2, color = 'green')
    plt.gca().set(title="", xlabel="", ylabel="")
    plt.close()

    # combine all fitted and predicted data
    growth_quantiles['Mean (Prediction invertal)'] = predicted_growth_df.mean(axis=1)
    all_data = fitted_values.join(growth_quantiles)
    return fig, all_data


def gdp_plot_and_data_bs(modelfit, pred_gdpGrowth, gdp_original, train, test, extra_test, predicted_gdp_df_bs, lower_q = 0.025, upper_q = 0.975):
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

    pred_gdp_data = pd.DataFrame(columns=['GDP Value',
                                                  'Prediction interval (2.5%)',
                                                  'Prediction interval (97.5%)',
                                                  'Mean (Prediction interval)'])
    # calcualte quantiles
    quantiles = predicted_gdp_df_bs.quantile(q=[lower_q, upper_q], axis=1, interpolation='linear')
    value_quantiles = np.transpose(quantiles)

    pred_gdp_data['GDP Value'] = predicted_GDP_df[0][1:]
    pred_gdp_data['Prediction interval (2.5%)'] = value_quantiles[lower_q]
    pred_gdp_data['Prediction interval (97.5%)'] = value_quantiles[upper_q]
    pred_gdp_data['Mean (Prediction interval)'] = predicted_gdp_df_bs.mean(axis=1)

    Actual_GDP = gdp_original['GDP'][1:]
    fittedandActual_GDP = pd.DataFrame({'Actual GDP': Actual_GDP,
                                        'Fitted GDP': fitted_GDP_df.squeeze(),
                                        'Predicted GDP': predicted_GDP_df.squeeze()
                                       })

    # plot
    fittedandActual_GDP.index = pd.to_datetime(fittedandActual_GDP.index)
    fig = plt.figure(figsize=(12, 4), dpi=100)
    plt.plot(fittedandActual_GDP, marker='o', markersize=4)
    plt.plot(predicted_gdp_df_bs.mean(axis=1), color='green', linestyle='--')
    plt.fill_between(value_quantiles.index, value_quantiles[lower_q], value_quantiles[upper_q], alpha = 0.2, color = 'green')
    plt.gca().set(title="", xlabel="", ylabel="")
    plt.close()

    # combine all fitted and predicted data
    value_quantiles['Mean (Prediction invertal)'] = predicted_gdp_df_bs.mean(axis=1)
    all_data = fittedandActual_GDP.join(value_quantiles)

    return fig, all_data

#################################################### RTS FUNCTIONS####################################################

def growth_rate_plot_and_data_RTS(predicted_growth_df=None,
                              lower_q = 0.025,
                              upper_q = 0.975,
                              modelfit= None, 
                              retailsales_final = None, 
                              train = None,
                              rf_pred_retailgrowth = None,
                              fitted_growthRate_rf = None):

    pred_growth_rate_data = pd.DataFrame(columns=['Retail Trade Sales Growth Rate',
                                                  'Prediction interval (2.5%)',
                                                  'Prediction interval (97.5%)',
                                                  'Mean (Prediction interval)'])
    # calcualte quantiles
    quantiles = predicted_growth_df.quantile(q=[0.025, 0.975], axis=1, interpolation='linear')
    growth_quantiles = np.transpose(quantiles)

    pred_growth_rate_data['Retail Trade Sales Growth Rate'] = rf_pred_retailgrowth
    pred_growth_rate_data['Prediction interval (2.5%)'] = growth_quantiles[lower_q]
    pred_growth_rate_data['Prediction interval (97.5%)'] = growth_quantiles[upper_q]
    pred_growth_rate_data['Mean (Prediction interval)'] = predicted_growth_df.mean(axis=1)

    # organise data for plot
    pred_rtsGrowth_for_plot = pd.concat([train['GrowthRate'].tail(1), rf_pred_retailgrowth])
    fitted_values = pd.DataFrame({'GrowthRate': retailsales_final['GrowthRate'],
                                'Fitted Value': fitted_growthRate_rf.squeeze(),
                                'Predicted Value': pred_rtsGrowth_for_plot.squeeze()})

    # plot
    fitted_values.index = pd.to_datetime(fitted_values.index)
    fig = plt.figure(figsize=(12, 4), dpi=100)
    plt.plot(fitted_values, marker='o', markersize=2)
    plt.plot(predicted_growth_df.mean(axis=1), color='green', linestyle='--')
    plt.fill_between(growth_quantiles.index, growth_quantiles[lower_q], growth_quantiles[upper_q], alpha = 0.2, color = 'green')
    plt.gca().set(title="", xlabel="", ylabel="")
    plt.close()
    
    # combine all fitted and predicted data
    growth_quantiles['Mean (Prediction invertal)'] = predicted_growth_df.mean(axis=1)
    all_data = fitted_values.join(growth_quantiles)
    
    return fig, all_data


def retail_plot_and_data_bs(modelfit, pred_retailGrowth, retailsales, train, test, extra_test, predicted_retail_df_bs, lower_q = 0.025, upper_q = 0.975):
    
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
        #print(f"Prediction error: {pred_error}")

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
    

    pred_retail_data = pd.DataFrame(columns=['Retail Sales Value',
                                                  'Prediction interval (2.5%)',
                                                  'Prediction interval (97.5%)',
                                                  'Mean (Prediction interval)'])
    # calcualte quantiles
    quantiles = predicted_retail_df_bs.quantile(q=[lower_q, upper_q], axis=1, interpolation='linear')
    value_quantiles = np.transpose(quantiles)

    pred_retail_data['Retail Sales Value'] = predicted_retail_df[0][1:]
    pred_retail_data['Prediction interval (2.5%)'] = value_quantiles[lower_q]
    pred_retail_data['Prediction interval (97.5%)'] = value_quantiles[upper_q]
    pred_retail_data['Mean (Prediction interval)'] = predicted_retail_df_bs.mean(axis=1)

    Actual_retail = retailsales['VALUE'][1:]
    fittedandActual_retail = pd.DataFrame({'Actual Retail Sales': Actual_retail,
                                        'Fitted Retail Sales': fitted_retail_df.squeeze(),
                                        'Predicted Retail Sales': predicted_retail_df.squeeze()
                                       })

    # plot
    fittedandActual_retail.index = pd.to_datetime(fittedandActual_retail.index)
    fig = plt.figure(figsize=(12, 4), dpi=100)
    plt.plot(fittedandActual_retail, marker='o', markersize=4)
    plt.plot(predicted_retail_df_bs.mean(axis=1), color='green', linestyle='--')
    plt.fill_between(value_quantiles.index, value_quantiles[lower_q], value_quantiles[upper_q], alpha = 0.2, color = 'green')
    plt.gca().set(title="", xlabel="", ylabel="")
    plt.close()
    
    # combine all fitted and predicted data
    value_quantiles['Mean (Prediction invertal)'] = predicted_retail_df_bs.mean(axis=1)
    all_data = fittedandActual_retail.join(value_quantiles)
    
    return fig, all_data


# E-commerce Bootstrap

def ecommerce_plot_and_data_bs(modelfit, pred_EcommerceGrowth, retailEcommercesales, train, test, extra_test, predicted_e_df_bs, lower_q = 0.025, upper_q = 0.975):
    # fitted gdp value for training set
    base_sales = retailEcommercesales['Ecommerce_sales'][1]
    
    # calculate fitted retail sales
    X_xgboost = train.loc[:, ~train.columns.isin(['Growth_rate'])]
    fitted_values = modelfit.predict(X_xgboost)  # fitted growth rate
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
        #print(f"Prediction error: {pred_error}")

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

    pred_e_data = pd.DataFrame(columns=['Predicted Ecommerce Value',
                                                  'Prediction interval (2.5%)',
                                                  'Prediction interval (97.5%)',
                                                  'Mean (Prediction interval)'])
    # calcualte quantiles
    quantiles = predicted_e_df_bs.quantile(q=[lower_q, upper_q], axis=1, interpolation='linear')
    value_quantiles = np.transpose(quantiles)

    pred_e_data['Predicted Ecommerce Value'] = predicted_sales_df[0][1:]
    pred_e_data['Prediction interval (2.5%)'] = value_quantiles[lower_q]
    pred_e_data['Prediction interval (97.5%)'] = value_quantiles[upper_q]
    pred_e_data['Mean (Prediction interval)'] = predicted_e_df_bs.mean(axis=1)

    Actual_Ecommerce = retailEcommercesales['Ecommerce_sales'][1:]
    fittedandActual_sales = pd.DataFrame({'Actual Ecommerce': Actual_Ecommerce,
                                        'Fitted Ecommerce': fitted_sales_df.squeeze(),
                                        'Predicted Ecommerce': predicted_sales_df.squeeze()
                                       })

    # plot
    fittedandActual_sales.index = pd.to_datetime(fittedandActual_sales.index)
    fig = plt.figure(figsize=(12, 4), dpi=100)
    plt.plot(fittedandActual_sales, marker='o', markersize=4)
    plt.plot(predicted_e_df_bs.mean(axis=1), color='green', linestyle='--')
    plt.fill_between(value_quantiles.index, value_quantiles[lower_q], value_quantiles[upper_q], alpha = 0.2, color = 'green')
    plt.gca().set(title="", xlabel="", ylabel="")
    plt.close()

    # combine all fitted and predicted data
    value_quantiles['Mean (Prediction invertal)'] = predicted_e_df_bs.mean(axis=1)
    all_data = fittedandActual_sales.join(value_quantiles)
    return fig, all_data