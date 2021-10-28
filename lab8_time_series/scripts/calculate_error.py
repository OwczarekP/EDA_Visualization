from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit

import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def read_dataframe(path, country):
    """read_dataframe
    This function load the csv file into dataframe
    Then it filter to show data only from one country,
    and shows the year as date

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    df = df.loc[df['Country'] == country]
    df = df[['year', 'AverageTemperatureCelsius']]
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    df = df.groupby(['year'], as_index=False).mean()
    return df


def sarima_cv(df, ordr, season):
    """sarima_cv
    This function create train and test dataset for sarima model
    The order and seasonal_order are provided by the user
    Then the model check the predicted value with actual values
    and calculate mean absolute error

    :param df: the dataframe with average temperature data
    :param ordr: the tuple with order values
    :param season: the tuple with seasonal_order values
    :return: absolute mean error
    """
    n_splits = 10
    tscv = TimeSeriesSplit(n_splits)
    X = df['year']
    y = df['AverageTemperatureCelsius']
    for train_index, test_index in tscv.split(X):
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    model_train = SARIMAX(y_train,
                                    order=ordr,
                                    seasonal_order= season,
                                    enforce_stationarity=False,
                                    enforce_invertibility=False).fit()
    predictions = model_train.forecast()
    true = df['AverageTemperatureCelsius'].reindex(predictions.index)
    return mean_absolute_error(true, predictions)


def whes_cv(df):
    """whes_cv
    This function create train and test dataset for whes model
    Then the model check the predicted value with actual values
    and calculate mean absolute error

    :param df: the dataframe with average temperature data
    :return: absolute mean error
    """
    n_splits = 10
    tscv = TimeSeriesSplit(n_splits)
    X = df['year']
    y = df['AverageTemperatureCelsius']
    for train_index, test_index in tscv.split(X):
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    model_train = ExponentialSmoothing(y_train, seasonal_periods=4, trend='add', seasonal='mul',
                               initialization_method="estimated").fit()
    predictions = model_train.forecast()
    true = df['AverageTemperatureCelsius'].reindex(predictions.index)
    return mean_absolute_error(true, predictions)


def ar_cv(df):
    """ar_cv
    This function create train and test dataset for ar model
    Then the model check the predicted value with actual values
    and calculate mean absolute error

    :param df: the dataframe with average temperature data
    :return: absolute mean error
    """
    n_splits = 10
    tscv = TimeSeriesSplit(n_splits)
    X = df['year']
    y = df['AverageTemperatureCelsius']
    for train_index, test_index in tscv.split(X):
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    model_train = AutoReg(y_train, lags=20).fit()
    predictions = model_train.forecast()
    true = df['AverageTemperatureCelsius'].reindex(predictions.index)
    return mean_absolute_error(true, predictions)


def main():
    df_jap = read_dataframe('../data/temperature_clean.csv', 'Japan')
    sarima_jap = sarima_cv(df_jap, (0, 1, 1), (1, 1, 2, 4))
    ar_jap = ar_cv(df_jap)
    whes_jap = whes_cv(df_jap)
    df_nzl = read_dataframe('../data/temperature_clean.csv', 'New Zealand')
    sarima_nzl = sarima_cv(df_nzl, (1, 1, 1), (0, 1, 1, 4))
    ar_nzl = ar_cv(df_nzl)
    whes_nzl = whes_cv(df_nzl)
    print('MAE for Japan in SARIMA model: %s' %(sarima_jap))
    print('MAE for Japan in AR model: %s' %(ar_jap))
    print('MAE for Japan in WHES model: %s' %(whes_jap))
    print('MAE for New Zealand in SARIMA model: %s' %(sarima_nzl))
    print('MAE for New Zealand in AR model: %s' %(ar_nzl))
    print('MAE for New Zealand in WHES model: %s' %(whes_nzl))


if __name__ == '__main__':
    main()