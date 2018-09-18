import pandas as pd
import re

from fdms.config.countries import COUNTRIES


AMECO = 'fdms/sample_data/AMECO_H.TXT'
FORECAST = 'fdms/sample_data/LT.Forecast.SF2018.xlsm'


# TODO: create get_series_noindex to get series from intermediate results (rangeindex instead of country and variable)
def get_series(dataframe, country_ameco, variable_code):
    '''Get quarterly or yearly data from dataframe with indexes "Country AMECO" and "Variable Code"'''
    dataframe.sort_index(level=[0, 1], inplace=True)
    series = dataframe.loc[(country_ameco, variable_code)].filter(regex='\d{4}')
    if series.empty:
        series = dataframe.loc[(country_ameco, variable_code)].filter(regex='\d{4}Q[1234]')
    if series.empty:
        return None
    # TODO: Log these and make sure that this is correct, check values and get the best one
    if len(series.shape) > 1:
        series = series.iloc[0]
    series = pd.to_numeric(series.squeeze(), errors='coerce')
    return series


def get_series_noindex(dataframe, country_ameco, variable_code, metadata=False):
    '''Get quarterly or yearly data from dataframe with default RangeIndex from "Country AMECO" and "Variable Code"'''
    result_series_index = dataframe.loc[(dataframe['Country Ameco'] == country_ameco) & (
            dataframe['Variable Code'] == variable_code)].index.values[0]
    series = dataframe.loc[result_series_index]
    series_meta = {'Country Ameco': series['Country Ameco'], 'Variable Code': series['Variable Code'],
                   'Frequency': series['Frequency'], 'Scale': series['Scale']}
    if metadata is True:
        return series_meta
    series = series.filter(regex='\d{4}')
    if series.empty:
        series = dataframe.loc[result_series_index].filter(regex='\d{4}Q[1234]')
    if series.empty:
        return None
    if len(series.shape) > 1:
        series = series.iloc[0]
    series = pd.to_numeric(series.squeeze(), errors='coerce')
    return series


def get_index(dataframe, country_ameco, variable_code):
    return dataframe.loc[(dataframe['Country Ameco'] == country_ameco) & (
            dataframe['Variable Code'] == variable_code)].index.values[0]


# TODO: also fix (two times this returns two series)
def get_scale(dataframe, country_ameco, variable_code):
    dataframe.sort_index(level=[0, 1], inplace=True)
    scale = dataframe.loc[(country_ameco, variable_code)]['Scale']
    if type(scale) == str:
        return scale
    return scale.squeeze()


def get_frequency(dataframe, country_ameco, variable_code):
    dataframe.sort_index(level=[0, 1], inplace=True)
    frequency = dataframe.loc[(country_ameco, variable_code)]['Frequency']
    if type(frequency) == str:
        return frequency
    return frequency.squeeze()


