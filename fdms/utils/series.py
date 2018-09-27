import pandas as pd
import re

from fdms.config.countries import COUNTRIES


AMECO = 'fdms/sample_data/AMECO_H.TXT'
FORECAST = 'fdms/sample_data/LT.Forecast.SF2018.xlsm'
VARS_FILENAME = 'output/outputvars.txt'
EXCEL_FILENAME = 'output/output.xlsx'
COLUMN_ORDER = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000,
                2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
                2018, 2019]


def get_series(dataframe, country_ameco, variable_code, metadata=False):
    '''Get quarterly or yearly data from dataframe with indexes "Country AMECO" and "Variable Code"'''
    dataframe.sort_index(level=[0, 1], inplace=True)
    if metadata is True:
        series = dataframe.loc[(country_ameco, variable_code)]
        frequency = series.get('Frequency') if series.get('Frequency') is not None else 'Annual'
        frequency = frequency if type(frequency) == str else frequency.name
        scale = series.get('Scale') if series.get('Scale') is not None else series.get('Unit of the series')
        scale = scale if type(scale) == str else scale.name
        series_meta = {'Country Ameco': country_ameco, 'Variable Code': variable_code, 'Frequency': frequency,
                       'Scale': scale}
        return series_meta
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


def export_to_excel(result, vars_filename=VARS_FILENAME, excel_filename=EXCEL_FILENAME, sheet_name='Sheet1'):
    column_order = COLUMN_ORDER
    export_data = result.copy()
    export_data = export_data.reset_index()
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                       sheet_name=sheet_name, index=False)
    result_vars = result.index.get_level_values('Variable Code').tolist()
    with open(vars_filename, 'w') as f:
        f.write('\n'.join(result_vars))

