import logging

import pandas as pd
import re

from fdms.utils.splicer import Splicer


logger = logging.getLogger(__name__)
logging.basicConfig(filename='error.log',
                    format='{%(pathname)s:%(lineno)d} - %(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)


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

    def rebase(self, series, base_period, bp1=False):
        new_series = pd.Series({base_period: 100})
        splicer = Splicer()
        return splicer.ratio_splice(new_series, series, kind='both')
