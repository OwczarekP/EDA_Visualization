import numpy as np
import pandas as pd
import argparse
from bokeh.io import export_png
from bokeh.models import Legend
from bokeh.plotting import figure, output_file, show, save


# List of parser command
parser = argparse.ArgumentParser(prog='Create plot', description='create plot and save/show it.')
parser.add_argument('-o', '--o', default='output-mode', type=int, nargs=1, choices=[0, 1],  help='Mode of output. 0 - show plot, 1- save plot')
parser.set_defaults(o=1)
args = parser.parse_args()

inpt = args.o[0]


def read_dataframe(path):
    """read_dataframe
    This function load the csv file into dataframe
    Additionaly it replace the no-data cells to NaN cells

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    df = df.T
    df = df.drop(['Jednostka'])
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df = df.replace('.', np.NaN)
    return df


def create_plot(df):
    """create_plot
    This function create the line plot
    Each species has one line

    :param df: dataframe with the slaughter livestock data
    :return:
    """
    p = figure(title="Production of slaughter livestock in Poland",
               x_axis_label='year', y_axis_label='production [t]',
               plot_width=1000, plot_height=550,
               )
    p.yaxis.formatter.use_scientific = False
    p.add_layout(Legend(), 'right')
    years = list(range(1946, 1999))
    p.line(years, df['bydło'].tolist(), legend_label="cattle", line_color="blue", line_width=2)
    p.line(years, df['cielęta'], legend_label="calves", line_color="red", line_width=2)
    p.line(years, df['trzoda chlewna'], legend_label="pig", line_color="fuchsia", line_width=2)
    p.line(years, df['owce'], legend_label="sheep", line_color="green", line_width=2)
    p.line(years, df['konie'], legend_label="horses", line_color="purple", line_width=2)
    p.line(years, df['drób'], legend_label="poultry", line_color="black", line_width=2)
    p.line(years, df['kozy i króliki'], legend_label="goats, rabbits", line_color="olive", line_width=2)
    p.legend.click_policy = "hide"
    p.title.text_font_size = "30px"
    p.legend.title = 'Livestock'

    if inpt == 0:
        show(p)
    elif inpt == 1:
        output_file('images/plot3.html')
        export_png(p, filename="images/plot3.png")
        save(p)
        print('Image saved in: ./images/plot3.png')
    else:
        raise Exception('incorrect command!')


def main():
    df = read_dataframe('./data/rolnictwo.csv')
    create_plot(df)


if __name__ == '__main__':
    main()