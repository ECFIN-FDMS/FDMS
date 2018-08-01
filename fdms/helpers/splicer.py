import logging
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


class Splicer:
    '''Provides methods to perform required calculations with pandas DataFrames'''

    def butt_splice(self, base_series, splice_series, kind='both', replace_empty_base_series=True, period=None):
        '''
        Splicing extends the ends of the base series with data values from another series. Splicing does not fill gaps
         within the base series.
        User can choose whether splicing should be applied:
            -  Backward, from the first observation of the base series
            -  Forward, from the last observation of the base series
            -  Both directions, from both ends of the base series
        A common usage of splicing is to extend the base series with series from other sources. One example is to
         extend series in the working database with historical data from the archive database.
        BUTTSPLICE extends the base series by taking the values directly from the splice series.

        :param base_series: Required. Specify a time series or an expression to be used as a base for splicing.
        :type base_series: pandas.core.frame.DataFrame
        :param splice_series: Required. Specify a time series or an expression where values are to be used for splicing
         purpose.
        :type splice_series: pandas.core.frame.DataFrame
        :param str kind: Optional. "forward", "Backward" or "both". Default = "both".
        :param bool replace_empty_base_series: TODO: Check if we need this one
        :param period: TODO: Check if we need this one
        :return:
        :rtype: pandas.core.frame.DataFrame
        '''
        # We assume both DataFrames have the same frequency for now

        result = base_series.copy()
        name = result.name
        if kind == 'forward' or kind == 'both':
            base_last_valid = base_series.last_valid_index()
            base_last_index = base_series.index[-1]
            splice_end = splice_series.last_valid_index()
            if base_last_valid > splice_end:
                logger.warning('Failed to splice {} forward, country {}, Splice series ends before base series').format(
                    base_series.name[0], base_series.name[1])
            else:
                base_last_valid_loc = base_series.index.get_loc(base_last_valid)
                forward_splice_start_loc = splice_series.index.get_loc(base_last_valid) + 1
                splice_end_loc = splice_series.index.get_loc(splice_end)
                result.iloc[base_last_valid_loc + 1:] = splice_series.iloc[forward_splice_start_loc:splice_end_loc]
                if splice_series.index[-1] > base_last_index:
                    splice_overflow_start_loc = splice_series.index.get_loc(base_last_index + 1)
                    result = result.append(splice_series.iloc[splice_overflow_start_loc:])

        if kind == 'backward' or kind == 'both':
            base_first_valid = base_series.first_valid_index()
            base_first_index = base_series.index[0]
            splice_start = splice_series.first_valid_index()
            if base_first_valid < splice_start:
                logger.warning('Failed to splice {}, country {}, Splice series starts after base series').format(
                    base_series.name[0], base_series.name[1])
            else:
                base_first_valid_loc = base_series.index.get_loc(base_first_valid)
                backward_splice_start_loc = splice_series.index.get_loc(base_first_index)
                splice_end_loc = splice_series.index.get_loc(base_first_valid - 1)
                result.iloc[:base_first_valid_loc - 1] = splice_series.iloc[backward_splice_start_loc:splice_end_loc]
                if splice_series.index[0] < base_first_index:
                    splice_overflow_end = splice_series.index.get_loc(base_first_index)
                    result = pd.concat([splice_series.iloc[:splice_overflow_end], result])
                    result.name = name

        return result