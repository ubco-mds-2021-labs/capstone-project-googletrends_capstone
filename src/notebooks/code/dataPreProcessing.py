import pandas as pd
from sklearn.model_selection import train_test_split


# make one dataframe of the passed predictors
def make_predictors_df(*arg):
    "joins the predictors dataframes"
    if len(arg) > 1:
        for i in range(0, len(arg)-1):
            if i == 0:
                arg[i].index = pd.to_datetime(arg[i].index)
                arg[i+1].index = pd.to_datetime(arg[i+1].index)
                predictors_df = pd.merge(arg[i], arg[i+1], left_index=True, right_index=True)
            else:
                predictors_df = pd.merge(predictors_df, arg[i+1], left_index=True, right_index=True)
    else:
        arg[0].index = pd.to_datetime(arg[0].index)
        return arg[0]
    return predictors_df


# split train and test set
def ts_train_test_split(response_df, predictors_df, test_size):
    " splits the train and test set and also returns the extra test data of predictors"
    # train test split
    joind_df = pd.merge(response_df, predictors_df, left_index=True, right_index=True)

    if test_size > 0:
        train, test = train_test_split(joind_df, test_size=test_size, shuffle=False)
        # extra test data
        extra_test_data = predictors_df.loc[predictors_df.index > joind_df.index[len(joind_df.index)-1], :]
        return train, test, extra_test_data
    elif test_size == 0:
        train = joind_df
        test = pd.DataFrame(data=None)
        # extra test data
        extra_test_data = predictors_df.loc[predictors_df.index > joind_df.index[len(joind_df.index)-1], :]
        return train, test, extra_test_data