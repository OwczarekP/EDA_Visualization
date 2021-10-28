"""
Data Analysis and Visualization, lab 2
Patrycja Owczarek
Script for animated plot creation:
Pick Poland and then find 4 other countries that are the closest by
population size (+2 or -2) in given year and do similar plot
"""

import matplotlib.pyplot as plt
import ffmpy
from matplotlib.animation import FuncAnimation
import pycountry as pc
import pandas as pd

global df
global years
fig, ax = plt.subplots(figsize=(12, 8))

years = list(range(1960, 2019))
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
    global years
    df = read_file(df)
    country_codes = list(df['Country Code'])
    to_delete = []
    for country in country_codes:
        if pc.countries.get(alpha_3=country) is None:
            to_delete.append(country)
    df = df[df['Country Code'].isin(to_delete) == False]
    df = df.drop(columns=['Indicator Code', 'Indicator Name', '2020','Unnamed: 65'])
    df = get_countries(df)
    df = df.set_index('Country Code')
    df = df.dropna()
    df = df.drop(columns='Country Name')
    df = df.loc[(df!=0).any(1)]
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].div(100000)
    return df

def get_countries(df):
    """get_countires

     This function read the dataframe. Then for every year it change the value of population:
     if the population is smaller or bigger than Poland and 2 closest bigger/smaller countries the
     population is changed to 0.

     Args:
         df (dataframe): dataframe contains the data from partial cleaning

     Returns:
         df (dataframe): the dataframe with population for only 4 countries closest in population o Poland
         """
    for col in df.columns[2:]:
        df = df.sort_values(by=col, ignore_index=True)
        ind = df.index[df['Country Code'] == 'POL'].tolist()
        start = ind[0]-3
        end = ind[0]+3
        df.loc[:start, col] = 0
        df.loc[end:, col] = 0
    return df



def create_plot(i):
    """create_plot

     This function read the dataframe and create the bar chart race plot:
     - x axis contains country, y axis population (in millions)
     - the plot shows only 5 countries
     - one year last exactly 500 ms
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
    df_year = df.sort_values(by=years[i], ascending=True)[-5:]
    c = pc = [ "|" , "/" , "+" , "-", ".", "*",
               "x", "o", "|-|" , "//" , "+.+" , "-||-",
               "...", "-\ ", '\/', ' \ \ ', 'o', ' //\ ',
               '+o', '*_', 'O','_._', '|*', '.-.' ]
    shapes = dict(zip(list(df.index),c[:len(df.index)]))
    shapes_year = [shapes[x] for x in list(df_year.index)]
    for x in range(0, 5):
        ax.bar(df_year.index[x], df_year[years[i]][x], color='white', hatch=shapes_year[x], edgecolor='black')
    ax.get_xaxis().set_ticks([])
    ax.set_ylabel('Population [100k]', fontsize=18, weight=600,)
    ax.set_ylim(0, 500)
    ax.set_title('Countries most similar to population of Poland', size=30, weight=400)
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
        inputs={"../images/fig6.mp4": None},
        outputs={"../images/fig6.gif": None})
    ff.run()


def main():
    global df
    global years
    df = clean_dataframe('../data/API_SP.POP.TOTL_DS2_en_csv_v2_2106202.csv')
    ani = FuncAnimation(fig, create_plot, frames=len(years))
    ani.save('../images/fig6.mp4', fps=3)
    save_gif()

if __name__ == "__main__":
    main()