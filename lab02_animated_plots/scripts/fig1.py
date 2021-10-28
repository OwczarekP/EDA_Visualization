"""
Data Analysis and Visualization, lab 2
Patrycja Owczarek
Script for animated plot creation:
Given the data from The Word Bank do animated bar plots (gif file) for all years for
5 most populated countries
"""

import matplotlib.pyplot as plt
import ffmpy
from matplotlib.animation import FuncAnimation
import pycountry as pc
import pandas as pd

global df
global years
fig, ax = plt.subplots(figsize=(12, 8))

years = list(range(1960, 2020))
years = [str(x) for x in years]


def read_file(df_path):
    """read_file

     This function read the .csv file and save it as the dataframe

     Args:
         df_path (str): string contains path to the .csv dataset

     Returns:
         df (dataframe): the dataframe contains all data from .csv file
         """
    df = pd.read_csv(df_path, sep=',', skiprows=3)
    return df


def clean_dataframe(df):
    """clean_dataframe

     This function clean the dataframe:
     - delete all non-country rows
     - delete unimportant columns
     - change population to millions
     - transpose the dataframe

     Args:
         df (dataframe): dataframe contains the data for cleaning

     Returns:
         df (dataframe): the dataframe cleaned of all unnecessary data
         """
    df = read_file(df)
    country_codes = list(df['Country Code'])
    to_delete = []
    for country in country_codes:
        if pc.countries.get(alpha_3=country) is None:
            to_delete.append(country)
    df = df[df['Country Code'].isin(to_delete) == False]
    df = df.drop(columns=['Indicator Code', 'Indicator Name', '2020','Unnamed: 65'])
    df = df.set_index('Country Code')
    df = df.dropna()
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].div(1000000)
    return df


def create_plot(i):
    """create_plot

     This function read the dataframe and create the bar chart race plot:
     - x axis contains country, y axis population (in millions)
     - the plot shows only 5 countries
     - the plot is saved as mp4 file in images folder

     Args:
         i (int): the number of frames (years)

     Returns:
         None
         """
    global df
    global years
    ax.clear()
    year = years[i]
    c = plt.cm.Dark2(range(8))
    colors = dict(zip(["IDN", "RUS", "USA", "IND", "CHN", "JPN", "BRA", 'PAK'],c))
    df_year = df.sort_values(by=years[i], ascending=True)[-5:]
    colors_year = [colors[x] for x in list(df_year.index)]
    ax.bar(df_year.index, df_year[years[i]], color=colors_year)
    ax.get_xaxis().set_ticks([])
    ax.set_ylabel('Population [mln]', fontsize=18, weight=600,)
    ax.set_ylim(0, 1500)
    ax.set_title('The most populated countires', size=40, weight=600)
    for i, (value, name) in enumerate(zip(df_year[years[i]], df_year.index)):
        ax.text(i+0.15, value, name, ha='right', weight=600, visible=True, fontsize=18)
    ax.text(0.05, 0.85, year, transform=ax.transAxes, size=46)


def save_gif():
    """save_gif

     This function read the created mp4 plot and convert it to gif file.
     The gif is saved in images folder

     Args:
         None

     Returns:
         None
         """
    ff = ffmpy.FFmpeg(
        inputs={"../images/fig1.mp4": None},
        outputs={"../images/fig1.gif": None})
    ff.run()


def main():
    global df
    global years
    df = clean_dataframe('../data/API_SP.POP.TOTL_DS2_en_csv_v2_2106202.csv')
    ani = FuncAnimation(fig, create_plot, frames=len(years))
    ani.save('../images/fig1.mp4')
    save_gif()


if __name__ == "__main__":
    main()


