import altair as alt
import argparse
import pandas as pd
from vega_datasets import data


# List of parser command
parser = argparse.ArgumentParser(prog='Create plot', description='create plot and save/show it.')
parser.add_argument('-o', '--o', default='output-mode', type=int, nargs=1, choices=[0, 1],  help='Mode of output. 0 - show plot, 1- save plot')
parser.set_defaults(o=1)
args = parser.parse_args()

inpt = args.o[0]


def read_dataframe(path):
    """read_dataframe
    This function load the csv file into dataframe and return only relevant column

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    return df[['state', 'fips', 'cases']]


def create_plot(df):
    """create_plot
    This function create the  US map plot
    Each state has the colour depending on the number of cases

    :param df: dataframe with the temperature data
    :return:
    """
    states = alt.topo_feature(data.us_10m.url, 'states')

    states = alt.Chart(states, title='Number of covid-19 cases by state on 06/04/2021').mark_geoshape(
        stroke='black',
    ).encode(
            color='cases:Q',
            tooltip=['state:N', 'cases:Q'],
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(df, 'fips', ['state', 'cases'])
        ).properties(
            width=700,
            height=500
        ).project(
            type='albersUsa'
        ).configure_title(
        fontSize=24
        ).configure_legend(
        gradientLength=400,
        titleFontSize=18,
        labelFontSize=15
        )

    if inpt == 0:
        states.show()
    elif inpt == 1:
        states.save('images/plot6.html')
        states.save("images/plot6.png")
        print('Image saved in: ./images/plot6.png')
    else:
        raise Exception('incorrect command!')


def main():
    df = read_dataframe('./data/covid-usa.csv')
    create_plot(df)


if __name__ == '__main__':
    main()