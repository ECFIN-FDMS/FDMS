import logging


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


class Calculator:
    '''Provides methods to perform required calculations with pandas DataFrames'''

    def splice(self, base_series, splice_series, method, kind='both', overlap=False, replace_empty_base_series=True,
               period=None):
        '''
        Splicing extends the ends of the base series with data values from another series. Splicing does not fill gaps
         within the base series.
        User can choose whether splicing should be applied:
            -  Backward, from the first observation of the base series
            -  Forward, from the last observation of the base series
            -  Both directions, from both ends of the base series
        A common usage of splicing is to extend the base series with series from other sources. One example is to
         extend series in the working database with historical data from the archive database.
        The following four options are available:
            -  Butt: splicing the actual values
            -  Level: splicing the period-over-period difference
            -  Ratio: splicing the period-over-period ratio
            -  YoY: splicing the same-period-over-year-ago ratio, not applicable for daily data
        Percent splice is available as a separate function

        :param base_series: Required. Specify a time series or an expression to be used as a base for splicing.
        :type base_series: pandas.core.frame.DataFrame
        :param splice_series: Required. Specify a time series or an expression where values are to be used for splicing
         purpose.
        :type splice_series: pandas.core.frame.DataFrame
        :param str method: Required. Specify one of the four methods:
            -  Butt
            -  Level
            -  Ratio
            -  YoY
        :param str kind: Optional. "forward", "Backward" or "both". Default = both.
        :param bool overlap: TODO: Check if we need this one
        :param bool replace_empty_base_series: TODO: Check if we need this one
        :param period: TODO: Check if we need this one
        :return:
        :rtype: pandas.core.frame.DataFrame
        '''
        # We assume both DataFrames have the same frequency for now
        result = base_series.copy()
        if kind == 'forward' or kind == 'both':
            base_end = base_series.last_valid_index()
            splice_end = splice_series.last_valid_index()
            if base_end > splice_end:
                logger.warning('Failed to splice {}, country {}, Splice series ends before base series').format(
                    base_series.name[0], base_series.name[1])
            else:
                base_end_loc = base_series.index.get_loc(base_end)
                forward_splice_start_loc = splice_series.index.get_loc(base_end_loc) + 1
                splice_end_loc = splice_series.index.get_loc(splice_end)
                if method == 'butt':
                    result.iloc[base_end_loc + 1:] = splice_series.iloc[forward_splice_start_loc:splice_end_loc]


        if kind == 'backward' or kind == 'both':
            base_start = base_series.first_valid_index()
            splice_start = splice_series.first_valid_index()
            if base_start < splice_start:
                logger.warning('Failed to splice {}, country {}, Splice series starts after base series').format(
                    base_series.name[0], base_series.name[1])
            else:
                base_start_loc = base_series.index.get_loc(base_start)
                backward_splice_start_loc = splice_series.index.get_loc(base_start_loc) + 1
                splice_end_loc = splice_series.index.get_loc(base_start_loc - 1)
                if method == 'butt':
                    result.iloc[:base_start_loc - 1] = splice_series.iloc[backward_splice_start_loc:splice_end_loc]
