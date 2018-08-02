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
    '''
    Splicing extends the ends of the base series with data values from another series. Splicing does not fill gaps
     within the base series.
    User can choose whether splicing should be applied:
        -  Backward, from the first observation of the base series
        -  Forward, from the last observation of the base series
        -  Both directions, from both ends of the base series
    A common usage of splicing is to extend the base series with series from other sources. One example is to
     extend series in the working database with historical data from the archive database.
    '''

    def _get_forward_splice_boundaries(self, base_series, splice_series):
        '''
        :return: tuple(base_last_valid_loc, base_last_index, forward_splice_start_loc, splice_end_loc) or None
        '''
        base_last_valid = base_series.last_valid_index()
        base_last_index = base_series.index[-1]
        splice_end = splice_series.last_valid_index()
        forward_splice_start_loc = None
        if base_last_valid < splice_end:
            base_last_valid_loc = base_series.index.get_loc(base_last_valid)
            try:
                forward_splice_start_loc = splice_series.index.get_loc(base_last_valid + 1)
            except KeyError:
                pass
            splice_end_loc = splice_series.index.get_loc(splice_end)
        if forward_splice_start_loc is not None:
            return base_last_valid_loc, base_last_index, forward_splice_start_loc, splice_end_loc
        return None

    def _get_backward_splice_boundaries(self, base_series, splice_series):
        '''
        :return: tuple(base_first_valid_loc, base_first_index, backward_splice_start_loc, splice_end_loc) or None
        '''
        base_first_valid = base_series.first_valid_index()
        base_first_index = base_series.index[0]
        splice_start = splice_series.first_valid_index()
        backward_splice_start_loc = None
        if base_first_valid > splice_start:
            base_first_valid_loc = base_series.index.get_loc(base_first_valid)
            try:
                backward_splice_start_loc = splice_series.index.get_loc(base_first_index)
            except KeyError:
                pass
            splice_end_loc = splice_series.index.get_loc(base_first_valid)
        if backward_splice_start_loc is not None:
            return base_first_valid_loc, base_first_index, backward_splice_start_loc, splice_end_loc
        return None

    def butt_splice(self, base_series, splice_series, kind='both', period=None):
        '''
        BUTTSPLICE extends the base series by taking the values directly from the splice series.

        :param base_series: Required. Specify a time series or an expression to be used as a base for splicing.
        :type base_series: pandas.core.frame.DataFrame
        :param splice_series: Required. Specify a time series or an expression where values are to be used for splicing
         purpose.
        :type splice_series: pandas.core.frame.DataFrame
        :param str kind: Optional. "forward", "Backward" or "both". Default = "both".
        :param period: TODO: We may need this one only for ratiosplice, if so we can remove it from here
        :rtype: pandas.core.frame.DataFrame
        '''
        # We assume both DataFrames have the same frequency for now

        result = base_series.copy(deep=True)
        name = result.name
        if kind == 'forward' or kind == 'both':
            forward_splice_boundaries = self._get_forward_splice_boundaries(base_series, splice_series)
            if forward_splice_boundaries is not None:
                base_last_valid_loc, base_last_index, forward_splice_start_loc, splice_end_loc = (
                    forward_splice_boundaries)
                result.iloc[base_last_valid_loc + 1:] = splice_series.iloc[forward_splice_start_loc:splice_end_loc + 1]
                if splice_series.index[-1] > base_last_index:
                    splice_overflow_start_loc = splice_series.index.get_loc(base_last_index + 1)
                    result = result.append(splice_series.iloc[splice_overflow_start_loc:])
                    result.name = name
            else:
                logger.warning('Failed to splice {} forward, country {}, splice series ends before base series'.format(
                    base_series.name[1], base_series.name[0]))

        if kind == 'backward' or kind == 'both':
            backward_splice_boundaries = self._get_backward_splice_boundaries(base_series, splice_series)
            if backward_splice_boundaries is not None:
                base_first_valid_loc, base_first_index, backward_splice_start_loc, splice_end_loc = (
                    backward_splice_boundaries)
                result.iloc[:base_first_valid_loc] = splice_series.iloc[backward_splice_start_loc:splice_end_loc + 1]
                if splice_series.index[1] < base_first_index:
                    splice_overflow_end = splice_series.index.get_loc(base_first_index)
                    result = pd.concat([splice_series.iloc[:splice_overflow_end], result])
                    result.name = name
            else:
                logger.warning('Failed to splice {} backward, country {}, splice starts after base series'.format(
                    base_series.name[1], base_series.name[0]))

        return result

    def ratio_splice(self, base_series, splice_series, kind='both', period=None):
        '''
        RATIOSPLICE extends the base series by taking the period-over-period ratio (percent change) in the splice
         series, and applying the ratio to the base series.
        '''
        get_loc = base_series.index.get_loc
        start, end = get_loc(base_series.first_valid_index()), get_loc(base_series.last_valid_index())
        result = base_series.iloc[start:end]
        name = result.name
        if kind == 'forward' or kind == 'both':
            forward_splice_boundaries = self._get_forward_splice_boundaries(base_series, splice_series)
            if forward_splice_boundaries is not None:
                base_last_valid_loc, base_last_index, forward_splice_start_loc, splice_end_loc = (
                    forward_splice_boundaries)
                pct_change = splice_series.iloc[forward_splice_start_loc - 1:splice_end_loc + 1].pct_change()[1:]
                new_data = pct_change.copy()
                for index, item in pct_change.iteritems():
                    new_data[index] = item * base_series.loc[index - 1]
                result = pd.concat([result, new_data])
            else:
                logger.warning('Failed to splice {} forward, country {}, splice series ends before base series'.format(
                    base_series.name[1], base_series.name[0]))

        if kind == 'backward' or kind == 'both':
            backward_splice_boundaries = self._get_backward_splice_boundaries(base_series, splice_series)
            if backward_splice_boundaries is not None:
                base_first_valid_loc, base_first_index, backward_splice_start_loc, splice_end_loc = (
                    backward_splice_boundaries)
                pct_change = splice_series.iloc[backward_splice_start_loc - 1:splice_end_loc + 1].pct_change()[1:]
                new_data = pct_change.copy()
                for index in reversed(pct_change.index):
                    new_data[index] = pct_change.loc[index] * base_series.loc[index + 1]
                result = pd.concat([result, new_data])
            else:
                logger.warning('Failed to splice {} backward, country {}, splice starts after base series'.format(
                    base_series.name[1], base_series.name[0]))

        return result
