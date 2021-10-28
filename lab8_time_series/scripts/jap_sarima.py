from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

import pandas as pd
from itertools import product
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


def optimize_sarima(parameters_list, d, D, s, exog):
    """optimize_sarima
    This function check all possible parameters for order and seasonal order
    and check which one gives the lowest AIC value.

    :param parameters_list: the all possible values for p, P, q, Q
    :param d: the value of d parameter
    :param D: the value of D parameter
    :param s: the value of s parameter
    :param exog: the column with the values for training model
    :return:
    """
    results = []
    for param in parameters_list:
        try:
            model = SARIMAX(exog['AverageTemperatureCelsius'], order=(param[0], d, param[1]), seasonal_order=(param[2], D, param[3], s)).fit(disp=-1)
        except:
            continue
        aic = model.aic
        results.append([param, aic])

    result_df = pd.DataFrame(results)
    result_df.columns = ['(p,q)x(P,Q)', 'AIC']
    result_df = result_df.sort_values(by='AIC', ascending=True).reset_index(drop=True)
    return result_df


def create_model(df):
    """create_model
    This function create sarima model, for the
    average temperature data
    The order and seasonal_order were calculated by optimize_sarima function

    :param df: the dataframe with the average temperature values
    :return:
    """
    mod = SARIMAX(df['AverageTemperatureCelsius'],
                                    order=(0, 1, 1),
                                    seasonal_order=(1, 1, 2, 4),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()
    return results


def create_plot(df, results):
    """create_plot
    this function create line plot
    One line is provided by the actual temperature data
    The other line is predicted by the model for previous and next years
    showing on the plot with 95% confidence interval

    :param df: the dataframe with the actual average temperature
    :param results: the trained sarima model
    :return:
    """
    pred_uc = results.get_forecast(steps=249)
    pred_ci = pred_uc.conf_int()
    ax = df['AverageTemperatureCelsius'].plot(label='observed', figsize=(10, 7))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_title('Average temperature by year - forecast for Japan \n SARIMA model')
    ax.set_ylabel('Average temperature')
    plt.legend(["predicted", "actual", '95% confidence interval'], loc=2,)
    plt.tight_layout()
    plt.savefig('../images/jap_sarima.png')

def main():
    p = range(0, 4, 1)
    q = range(0, 4, 1)
    P = range(0, 4, 1)
    Q = range(0, 4, 1)
    parameters = product(p, q, P, Q)
    parameters_list = list(parameters)
    df = read_dataframe('../data/temperature_clean.csv')
    check_stationary(df)
    optimize_sarima(parameters_list, 1, 1, 4, df)
    results = create_model(df)
    create_plot(df, results)


if __name__ == '__main__':
    main()