import altair as alt
import argparse
import pandas as pd
import numpy as np

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
    return df[['seed']]


def create_plot(df):
    """create_plot
    This function create the histogram with the occurrence of number of sequences
    in seed in Pfam Database

    :param df: dataframe with the temperature data
    :return:
    """


    brush = alt.selection_interval(encodings=['x'])

    base = alt.Chart(df,  title='Histogram of sequences in Pfam database').mark_bar().encode(
    alt.X("seed:Q", bin=True, title='Number of sequences'),
    y='count()',
    )
    alternative = alt.vconcat(
      base.encode(
        alt.X('seed:Q',
          bin=alt.Bin(maxbins=30, extent=brush),
          scale=alt.Scale(domain=brush),
        title='Number of sequences'
        )
      ),
      base.encode(
        alt.X('seed:Q', bin=alt.Bin(maxbins=30),
          title='Number of sequences')
      ).add_selection(brush)
    ).configure_title(
        fontSize=20
        )

    if inpt == 0:
        alternative.show()
    elif inpt == 1:
        alternative.save('images/plot5.html')
        base.save("images/plot5.png")
        print('Image saved in: ./images/plot5.png')
    else:
        raise Exception('incorrect command!')


def main():
    df = read_dataframe('./data/pfam-seq.csv')
    create_plot(df)


if __name__ == '__main__':
    main()