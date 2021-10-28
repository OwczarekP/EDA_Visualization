from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
import warnings
from statsmodels.tsa.holtwinters import ExponentialSmoothing


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
    df = df.loc[df['Country'] == 'New Zealand']
    df=df[['year', 'AverageTemperatureCelsius']]
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
    This function create hwes model, for the
    average temperature data

    :param df: the dataframe with the average temperature values
    :return:
    """
    model = ExponentialSmoothing(df['AverageTemperatureCelsius'], seasonal_periods=4, trend='add', seasonal='mul',
                               initialization_method="estimated")
    results = model.fit()
    return results


def create_plot(df, results):
    """create_plot
    this function create line plot
    One line is provided by the actual temperature data
    The other line is predicted by the model for previous and next years
    showing on the plot with 50 others simulation(grey lines)

    :param df: the dataframe with the actual average temperature
    :param results: the trained hwes model
    :return:
    """
    simulations = results.simulate(249, repetitions=50, error='mul')

    ax = df['AverageTemperatureCelsius'].plot(figsize=(10, 7), color='red')
    ax = simulations.plot(ax=ax, style='-', alpha=0.05, color='grey', legend=False)
    ax = results.fittedvalues.plot(ax=ax, color='green')
    ax = results.forecast(249).plot(ax=ax, alpha=0.8, color='green',
                                                                   legend=True)
    ax.set_xlabel('Date')
    ax.set_title('Average temperature by year - forecast for New Zealand  \n HWES model')
    ax.set_ylabel('Average temperature')
    ax.set_xlim(30, 270)
    legend_elements = [Line2D([0], [0], color='red', lw=4, label='Line'),
                       Line2D([0], [0], color='green', lw=4, label='Line'),
                       Line2D([0], [0], color='grey', lw=4, label='Line')]
    plt.legend(legend_elements, ['actual', 'prediction', 'simulations'], loc=2)
    plt.tight_layout()
    plt.savefig('../images/nzl_hwes.png')


def main():
    df = read_dataframe('../data/temperature_clean.csv')
    check_stationary(df)
    results = create_model(df)
    create_plot(df, results)


if __name__ == '__main__':
    main()