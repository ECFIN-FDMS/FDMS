import logging

import pandas as pd
import re


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s', level=logging.INFO)


def get_series(dataframe, country_ameco, variable_code):
    '''Get quarterly or yearly data from dataframe with indexes "Country AMECO" and "Variable Code"'''
    dataframe.sort_index(level=1, inplace=True)
    series = dataframe.loc[(country_ameco, variable_code)].filter(regex='\d{4}')
    if series.empty:
        series = dataframe.loc[(country_ameco, variable_code)].filter(regex='\d{4}Q[1234]')
    if series.empty:
        return None
    # TODO: Log these and make sure that this is correct, check values and get the best one
    if len(series.shape) > 1:
        series = series.iloc[0]
    series = series.squeeze()
    return series

# TODO: also fix (two times this returns two series)
def get_scale(dataframe, country_ameco, variable_code):
    dataframe.sort_index(level=1, inplace=True)
    scale = dataframe.loc[(country_ameco, variable_code)]['Scale']
    if type(scale) == str:
        return scale
    return scale.squeeze()


def get_frequency(dataframe, country_ameco, variable_code):
    dataframe.sort_index(level=1, inplace=True)
    frequency = dataframe.loc[(country_ameco, variable_code)]['Frequency']
    if type(frequency) == str:
        return frequency
    return frequency.squeeze()


def read_raw_data(country_forecast_filename, ameco_filename, ameco_sheet_name, frequency='annual'):
    sheet_name = 'Transfer FDMS+ Q' if frequency == 'quarterly' else 'Transfer FDMS+ A'
    df = pd.read_excel(country_forecast_filename, sheet_name=sheet_name, header=10, index_col=[1, 3])
    ameco_df = pd.read_excel(ameco_filename, sheet_name=ameco_sheet_name, index_col=[0, 1])
    ameco_df.rename(columns={c: int(c) for c in ameco_df.columns if re.match('^\d+$', c)}, inplace=True)
    return df, ameco_df


class Operators:
    '''
    Merge, Iin, PCH
    '''
    def merge(self, dataframe):
        '''
        This function merges values from all the series in a dataframe, based on its sequence, taking the first not null
         value. The MERGE function can be used to combine data values and observation metadata.
        The MERGE function combines values to fill gaps and extends values on both ends of the series, between
         Calculation start and end periods. A common usage for the function is to combine values from different sources.
        :param args: Series to merge.
        :return:
        '''
        return dataframe.bfill(axis=0).iloc[0, :].filter(regex='\d{4}')

    def iin(self, series, value_if_null, value_if_not_null=None):
        '''
        Iin evaluates the input on a per-observation level, and returns one value if an individual observation is
         empty, and another value if not.
        :param series: Required.
        :param value_if_null: Required.
        :param value_if_not_null: Optional. if not present it will return the original value in the output.
        :return:
        '''
        if value_if_not_null is not None:
            series = series.where(series.isna(), value_if_not_null)
        return series.where(series.notna(), value_if_null)

    def pch(self, series):
        return series.pct_change() * 100
