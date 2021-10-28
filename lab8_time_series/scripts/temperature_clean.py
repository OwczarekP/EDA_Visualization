import pandas as pd


def read_dataframe(path):
    """read_dataframe
    This function load the csv file into dataframe

    :param path: string to the csv file
    :return: df: dataframe with the csv file
    """
    df = pd.read_csv(path)
    return df


def clean_na(df):
    """clean_na
    This function delete all rows with missing file

    :param df: the dataframe to the temperature data
    :return: df: the dataframe to the temperature data without missing rows
    """
    df = df.dropna()
    return df


def clean_day(df):
    """clean_day
    This function delete the 'day' column

    :param df: the dataframe to the temperature data
    :return: df: the dataframe with the temperature data without day column
    """
    df.pop("day")
    return df

def change_month(df):
    df["month"] = df.month.map("{:02}".format)
    return df

def convert_temp(df):
    """convert_temp
    This function create the new column with celsius data corresponding to the
    column with fahrenheit data

    :param df: the dataframe with the temperature data
    :return: df: the dataframe with the new celsius data
    """
    df["AverageTemperatureCelsius"] = fahr_to_celsius(df["AverageTemperatureFahr"])
    df["AverageTemperatureUncertaintyCelsius"] = fahr_to_celsius(df["AverageTemperatureUncertaintyFahr"])
    print(df.info())
    return df


def fahr_to_celsius(fahr):
    """fahr_to_celsius
    This function convert the fahrenheit temperature to the celsius temperature

    :param fahr: the value of fahrenheit temperature
    :return: cels: the value of celsius temperature
    """
    celc = round((fahr - 32) * 5 / 9, 4)
    return celc


def create_date(df):
    """create_date
    This function create year-month-day date with the month and year in the row

    :param df: the dataframe with the month and year column
    :return: df: dataframe with the new date column with yyyy-mm-dd date
    """
    df['date'] = pd.to_datetime([f'{y}-{m}-01' for y, m in zip(df.year, df.month)], format='%Y-%m-%d')
    return df


def main():
    df = read_dataframe('../data/temperature.csv')
    df = clean_na(df)
    df = clean_day(df)
    df = convert_temp(df)
    df = change_month(df)
    df = create_date(df)
    df.to_csv('../data/temperature_clean.csv')


if __name__ == '__main__':
    main()