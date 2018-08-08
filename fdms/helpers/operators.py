import logging
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s', level=logging.INFO)


def get_series(dataframe, country_ameco, variable_code):
    '''Get quarterly or yearly data from dataframe with indexes "Country AMECO" and "Variable Code"'''
    series = dataframe.loc[(country_ameco, variable_code)].filter(regex='\d{4}')
    if series.empty:
        series = dataframe.loc[(country_ameco, variable_code)].filter(regex='\d{4}Q[1234]')
    if series.empty:
        return None
    return series


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
