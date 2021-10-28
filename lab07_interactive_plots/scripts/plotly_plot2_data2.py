import pandas as pd
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
    This function load the csv file into dataframe.

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    return df


def clean_dataframe(df):
    """clean_dataframe
    This function search for unique genres, and count how any time they appears in the dataframe

    :param df: the dataframe to the IMDB data
    :return: df: dataframe with the cleaned genre column
    """
    genres_list = df['Genre'].unique()
    genres = []
    for g in genres_list:
        if ', ' in g:
            g = g.split(', ')
            for x in g:
                if x not in genres: genres.append(x)
        else:
            genres.append(g)
    genres_count = []
    for genre in genres:
        nb = df['Genre'].str.contains(genre).value_counts()[True]
        genres_count.append(nb)
    df_dict = {'Genre': genres, 'Number of titles': genres_count}
    df = pd.DataFrame(df_dict)
    return df


def create_plot(df):
    """create_plot
    This function create the pie plot
    each genre is individual group with value of appearing in the data


    :param df: dataframe with the temperature data
    :return: None
    """
    global inpt
    fig = px.pie(df, values='Number of titles', names='Genre')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig.update_layout(
        title={
            'text': 'IMDB top 1000 movies - genre'})
    fig.update_layout(legend=dict(
        yanchor="top",
        y=1.0,
        xanchor="right",
        x=0.01
    ))

    if inpt == 0:
        fig.show()
    elif inpt == 1:
        fig.write_html('./images/plot2.html')
        fig.write_image("images/plot2.png",  scale=1, width=1000, height=800)
        print('Image saved in: ./images/plot2.png')
    else:
        raise Exception('incorrect command!')

def main():
    df = read_dataframe('./data/imdb_top_1000.csv')
    df = clean_dataframe(df)
    create_plot(df)


if __name__ == '__main__':
    main()