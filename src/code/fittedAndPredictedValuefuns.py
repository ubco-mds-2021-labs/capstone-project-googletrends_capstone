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
