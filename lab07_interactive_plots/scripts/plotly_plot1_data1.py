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
    This function load the csv file into dataframe
    Additionally it remove the incorrect labeled rows in gender column

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    df = df.dropna()
    df = df.loc[(df['sex'] == 'FEMALE') | (df['sex'] == 'MALE')]
    return df


def create_plot(df):
    """create_plot
    This function create the box plot
    Each Species has two boxes: for female and male body mass

    :param df: dataframe with the  penguin data
    :return:
    """
    global inpt
    fig = px.box(df, x="species", y="body_mass_g",  color="sex",
                 width=800, height=700, template='plotly_white')
    fig.update_traces(quartilemethod="exclusive")
    fig.update_xaxes(
        title_text="Species",
        title_font={"size": 20},
        title_standoff=25)
    fig.update_layout(title_font_size=30)
    fig.update_layout(
        title={
            'text': 'Penguin body mass'})
    fig.update_yaxes(
        title_text="Body mass [g]",
        title_font={"size": 20},
        title_standoff=25)
    if inpt == 0:
        fig.show()
    elif inpt == 1:
        fig.write_html('./images/plot1.html')
        fig.write_image("images/plot1.png")
        print('Image saved in: ./images/plot1.png')
    else:
        raise Exception('incorrect command!')

def main():
    df = read_dataframe('./data/penguins_size.csv')
    create_plot(df)


if __name__ == '__main__':
    main()