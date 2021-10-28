import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import argparse

# List of parser command
parser = argparse.ArgumentParser(prog='Create plot', description='create plot and save/show it.')
parser.add_argument('-o', '--o', default='output-mode', type=int, nargs=1, choices=[0, 1],  help='Mode of output. 0 - show plot, 1- save plot')
parser.set_defaults(o=1)
args = parser.parse_args()

inpt = args.o[0]


def read_dataframe(path):
    """read_dataframe
    This function load the csv file into dataframe

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    return df


def get_average(df):
    """get_average
    This function count the average temperature for each year for each country

    :param df: the dataframe with the temperature data
    :return: result_df: dataframe with year, month-year date, average temperature and city column
    """
    df = df.loc[df['Country'] == 'South Africa']
    df = df[['year', 'date', 'AverageTemperatureCelsius']]
    return df


def create_plot(df):
    """create_plot
    This function create the scatter plot
    each color correspond to different city
    with month-year date at the x-axis and average temperature column as y-axis
    Then it shows it to the user or save two figures:
    html with the interactive plot showing monthly differences
    png with the yearly plot

    :param df: datafram with the date and temperature for cities
    """
    global inpt
    df = df.groupby(['date'], as_index=False).mean()
    fig = px.scatter(df, x='date', y="AverageTemperatureCelsius",
                     template='plotly_white', title='Average temperature for South Africa by month')
    if inpt == 0:
        fig.show()
    elif inpt == 1:
        fig.write_html('./images/fig5.html')
        create_yearly_plot(df)
        print('Image save in: ./images/fig5.png')
    else:
        raise Exception('incorrect command!')


def create_yearly_plot(df):
    """create_yearly_plot
    This function create the scatter plot
    each color correspond to different city
    with year date at the x-axis and average temperature column as y-axis
    then it save the plot as png file

    :param df: datafram with the date and temperature for cities
    """
    df = df.groupby(['year'], as_index=False).mean()
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(df['year'], df['AverageTemperatureCelsius'], linewidth=1)
    ax.grid(True, linewidth=1, color='lightgrey', linestyle='-')
    ax.set_axisbelow(True)
    ax.set_title('South Africa')
    fig.autofmt_xdate(rotation=30)
    fig.supxlabel('year', fontsize=16, weight=200)
    fig.suptitle('Average temperature', fontsize=22, weight=500)
    fig.supylabel('countryAverage', fontsize=16, weight=200)
    plt.tight_layout()
    plt.savefig('./images/fig5.png')


def main():
    df = read_dataframe('./data/temperature_clean.csv')
    result_df = get_average(df)
    create_plot(result_df)

if __name__ == '__main__':
    main()