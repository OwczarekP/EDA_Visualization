from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def read_dataframe(path):
    """read_dataframe
    This function load the csv file into dataframe
    Then it filter to show data only from one country,
    and shows the year as date and as an index

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    df = df.loc[df['Country'] == 'Japan']
    df = df[['year', 'AverageTemperatureCelsius']]
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    df = df.groupby(['year'], as_index=True).mean()
    return df


def check_stationary(df):
    """check stationary
    This function check if the provided data are stationary
    Ho: our data are non-stationary
    H1: our data are stationary
    To check this we use adfuller test

    :param df: the dataframe with average temperature
    """
    result = adfuller(df['AverageTemperatureCelsius'])
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))


def create_model(df):
    """create_model
    This function create autoregression model, for the
    average temperature data
    The lags 20 were chosen to have the lowest AIC

    :param df: the dataframe with the average temperature values
    :return:
    """
    model = AutoReg(df['AverageTemperatureCelsius'], lags=20)
    results = model.fit()
    return results


def create_plot(df, results):
    """create_plot
    this function create line plot
    One line is provided by the actual temperature data
    The other line is predicted by the model for previous and next years
    showing on the plot with 95% confidence interval

    :param df: the dataframe with the actual average temperature
    :param results: the trained autoregression model
    :return:
    """
    fig, ax = plt.subplots(figsize=(10, 15))
    fig = results.plot_predict(start=0, end=400)
    fig.suptitle('Average temperature by year - Japan \n Autoregression model')
    df['AverageTemperatureCelsius'].plot(label='observed', alpha=0.5)
    plt.legend(["predicted", "actual", '95% confidence interval'], loc=2,)
    plt.xlabel('date')
    plt.ylabel('Average temperature')
    plt.tight_layout()
    plt.savefig('../images/jap_ar.png')


def main():
    df = read_dataframe('../data/temperature_clean.csv')
    check_stationary(df)
    results = create_model(df)
    create_plot(df, results)


if __name__ == '__main__':
    main()