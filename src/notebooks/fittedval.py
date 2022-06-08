import pandas as pd
import numpy as np
import plots

class fit():
    def fitted_and_predicted_sales_randomForest(modelfit, pred_EcommerceGrowth, retailEcommercesales, train, test, extra_test):
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
        fig = plots.plots.plot_df(fittedandActual_sales, width=10, height=3)
        return pred_error, fig, fittedandActual_sales