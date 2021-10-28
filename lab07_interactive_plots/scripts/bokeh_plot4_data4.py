import pandas as pd
import argparse
from bokeh.io import export_png
from bokeh.models import LinearColorMapper, ColorBar, BasicTicker, HoverTool
from bokeh.palettes import Viridis256
from bokeh.transform import transform
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

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    return df


def clean_dataframe(df):
    """clean_dataframe
    This function replace the weather code with the weather name
    Additionally it return the average sharing for the same weather and temperature

    :param df: dataframe with the csv file
    :return:
    """
    df['weather_code'] = df['weather_code'].replace(1.0, 'clear')
    df['weather_code'] = df['weather_code'].replace(2.0, 'few clouds')
    df['weather_code'] = df['weather_code'].replace(3.0, 'broken clouds')
    df['weather_code'] = df['weather_code'].replace(4.0, 'cloudy')
    df['weather_code'] = df['weather_code'].replace(7.0, 'rain')
    df['weather_code'] = df['weather_code'].replace(10.0, 'thunderstorm')
    df['weather_code'] = df['weather_code'].replace(26.0, 'snowfall')
    df['weather_code'] = df['weather_code'].replace(94.0, 'freezing fog')
    df_cut = df.groupby(['t1','weather_code'])['cnt'].mean().reset_index()
    df_cut['cnt_scaled']= df['cnt'].div(100)
    return df_cut


def create_plot(df):
    """create_plot
    This function create the bubble plot
    with temperature at the x-axis and weather as y-axis
    Size of the bubble plot depend on number of sharing

    :param df: dataframe with the temperature data
    :return: None
    """
    p = figure(title="London bike sharing",
               x_axis_label='temperature', y_axis_label='weather',
               plot_width=1000, plot_height=550,
                y_range=df['weather_code'].unique()
               )
    color_mapper = LinearColorMapper(palette=Viridis256, low=df['cnt'].min(), high=df['cnt'].max())
    color_bar = ColorBar(color_mapper=color_mapper,
                         location=(0, 0),
                         ticker=BasicTicker())
    p.add_layout(color_bar, 'right')
    p.scatter(x='t1', y='weather_code', size='cnt_scaled', fill_color=transform('cnt', color_mapper),
                source=df, alpha=0.5)
    p.title.text_font_size = "30px"
    p.legend.title = 'Bike shares'
    p.add_tools(HoverTool(tooltips=[('Count', '@cnt')]))

    if inpt == 0:
        show(p)
    elif inpt == 1:
        output_file('images/plot4.html')
        export_png(p, filename="images/plot4.png")
        save(p)
        print('Image saved in: ./images/plot4.png')
    else:
        raise Exception('incorrect command!')


def main():
    df = read_dataframe('./data/london_merged.csv')
    df = clean_dataframe(df)
    create_plot(df)


if __name__ == '__main__':
    main()