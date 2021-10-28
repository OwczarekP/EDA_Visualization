"""
Data Analysis and Visualization, lab 2
Patrycja Owczarek
Script for animated plot creation:
Given the data from The Word Bank do animated dot plots (gif file) for all years for
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
    df = df.drop(columns=['Indicator Code', 'Indicator Name', '2020','Unnamed: 65', 'Country Name'])
    df = df.dropna()
    df = df.T
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df = df.div(1000000)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(float)
    df = df.sort_values(by='1960', axis=1, ascending=True).iloc[:,-5:]
    return df



def create_plot(i):
    """create_plot

     This function read the dataframe and create the animated dot plot:
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
    df_year = df.iloc[:i+1,:]
    ax.plot(df_year.index, df_year.values, 'o', alpha=0.3)
    ax.set_xlabel('Year', fontsize=18, weight=600,)
    ax.set_ylabel('Population [mln]', fontsize=18, weight=600,)
    ax.set_ylim(0, 1500)
    ax.set_xlim(0, 60)
    ax.set_xticks(range(0, 60, 10))
    ax.set_xticklabels(str(x) for x in (range(1960, 2020, 10)))
    ax.set_title('The most populated countries', size=40, weight=600)
    for i, (name, value) in enumerate(zip(df_year.columns, df_year.loc[years[i],:])):
        ax.text(len(df_year.axes[0])+3, value+0.3, name, ha='right', weight=300, visible=True, fontsize=14)
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
        inputs={"../images/fig13.mp4": None},
        outputs={"../images/fig13.gif": None})
    ff.run()


def main():
    global df
    global years
    df = clean_dataframe('../data/API_SP.POP.TOTL_DS2_en_csv_v2_2106202.csv')
    ani = FuncAnimation(fig, create_plot, frames=len(years))
    ani.save('../images/fig13.mp4')
    save_gif()


if __name__ == "__main__":
    main()


