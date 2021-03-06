import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='error.log',
                    format='{%(pathname)s:%(lineno)d} - %(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)

import pandas as pd


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

    def _strip_nan(self, series, direction='both'):
        try:
            start, end = series.index.get_loc(series.first_valid_index()), series.index.get_loc(
                series.last_valid_index())
        except KeyError:
            # TODO: Check why we get empty series here sometimes
            logger.warning('Series {} seems to be empty'.format(series.name))
            return series
        if direction == 'forward':
            return series.iloc[:end + 1]
        elif direction == 'backward':
            return series.iloc[start:]

    def _strip_and_get_forward_splice_boundaries(self, base_series, splice_series):
        '''
        :return: tuple(stripped_base_series, stripped_splice_series, start_splice_loc) or (None, None, None)
        '''
        stripped_base = self._strip_nan(base_series, direction='forward')
        stripped_splice = self._strip_nan(splice_series, direction='forward')
        if stripped_base.index[-1] < stripped_splice.index[-1] and stripped_base.index[-1] in stripped_splice.index:
            return stripped_base, stripped_splice, stripped_splice.index.get_loc(stripped_base.index[-1])
        return None, None, None

    def _strip_and_get_backward_splice_boundaries(self, base_series, splice_series):
        '''
        :return: tuple(stripped_base_series, stripped_splice_series, greater_splice_loc) or (None, None, None)
        '''
        stripped_base = self._strip_nan(base_series, direction='backward')
        stripped_splice = self._strip_nan(splice_series, direction='backward')
        if stripped_base.index[0] > stripped_splice.index[0] and stripped_base.index[0] in stripped_splice.index:
            return stripped_base, stripped_splice, stripped_splice.index.get_loc(stripped_base.index[0])
        return None, None, None

    def butt_splice(self, base_series, splice_series, kind='forward', period=None):
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
        if base_series is None:
            logger.warning('No historical data for {} to butt_splice, country {}, using country forecast '
                           'data.'.format(splice_series.name[1], splice_series.name[0]))
            return splice_series
        name = base_series.name
        result = None
        if kind == 'forward' or kind == 'both':
            stripped_base, stripped_splice, start_splice_loc = self._strip_and_get_forward_splice_boundaries(
                base_series, splice_series)
            if start_splice_loc is not None:
                result = pd.concat([stripped_base, splice_series.iloc[start_splice_loc + 1:]], sort=True)
                result.name = name
            else:
                variable, country = 'unknown', 'unknown'
                if type(base_series.name) == tuple:
                    variable, country = base_series.name[1], base_series.name[0]
                logger.warning('Failed to splice {} forward, country {}, splice series ends before base series'.format(
                    variable, country))
                return base_series

        if kind == 'backward' or kind == 'both':
            stripped_base, stripped_splice, greater_splice_loc = self._strip_and_get_backward_splice_boundaries(
                base_series, splice_series)
            stripped_result = stripped_base
            if result is not None:
                stripped_result = result.iloc[result.index.get_loc(stripped_base.index[0]):]
            if greater_splice_loc is not None:
                result = pd.concat([splice_series.iloc[:splice_series.index.get_loc(stripped_splice.index[5])],
                                    stripped_result], sort=True)
                result.name = name
            else:
                variable, country = 'unknown', 'unknown'
                if type(base_series.name) == tuple:
                    variable, country = base_series.name[1], base_series.name[0]
                logger.warning('Failed to splice {} forward, country {}, splice series ends before base series'.format(
                    variable, country))
                return base_series

        return result

    def ratio_splice(self, base_series, splice_series, kind='forward', variable=None, period=None, bp=False):
        '''
        RATIOSPLICE extends the base series by taking the period-over-period ratio (percent change) in the splice
         series, and applying the ratio to the base series.
        '''
        if base_series is None:
            logger.warning('No historical data for {} to ratio_splice, country, using country forecast '
                           'data.'.format(variable or 'Unknown variable'))
            return splice_series
        name = base_series.name
        result = None
        if kind == 'forward' or kind == 'both':
            stripped_base, stripped_splice, start_splice_loc = self._strip_and_get_forward_splice_boundaries(
                base_series, splice_series)
            if start_splice_loc is not None:
                pct_change = stripped_splice.iloc[start_splice_loc - 1:].pct_change()[1:]
                new_data = pct_change[1:].copy()
                new_data.iloc[0] = float(stripped_base.iloc[-1]) * (new_data.iloc[0] + 1)
                for index, item in list(pct_change.iteritems())[2:]:
                    new_data.loc[index] = new_data.loc[index - 1] * (item + 1)
                result = pd.concat([stripped_base, new_data, splice_series.iloc[splice_series.index.get_loc(
                    stripped_splice.index[-1]) + 1:]], sort=True)
                result.name = name
            else:
                variable, country = 'unknown', 'unknown'
                if type(base_series.name) == tuple:
                    variable, country = base_series.name[1], base_series.name[0]
                logger.warning('Failed to splice {} forward, country {}, splice series ends before base series'.format(
                    variable, country))
                if kind == 'forward':
                    return base_series

        if kind == 'backward' or kind == 'both':
            stripped_base, stripped_splice, greater_splice_loc = self._strip_and_get_backward_splice_boundaries(
                base_series, splice_series)
            stripped_result = stripped_base
            if result is not None:
                stripped_result = result.iloc[result.index.get_loc(stripped_base.index[0]):]
            if greater_splice_loc is not None:
                pct_change = stripped_splice.iloc[:greater_splice_loc + 2].pct_change()[:-1]
                new_data = pct_change[:-1].copy()
                new_data.iloc[-1] = stripped_base.iloc[0] / (pct_change.iloc[-1] + 1)
                for index, item in list(reversed(list(pct_change.iteritems())))[1:-1]:
                    new_data.loc[index - 1] = new_data.loc[index] / (item + 1)
                result = pd.concat([splice_series.iloc[:splice_series.index.get_loc(
                    stripped_splice.index[0])], new_data, stripped_result], sort=True)
                result.name = name
            else:
                variable, country = 'unknown', 'unknown'
                if type(base_series.name) == tuple:
                    variable, country = base_series.name[1], base_series.name[0]
                logger.warning('Failed to splice {} backward, country {}, splice series ends before base series'.format(
                    variable, country))
                if kind == 'backward':
                    return base_series

        return result

    def level_splice(self, base_series, splice_series, kind='forward', period=None):
        '''
        LEVELSPLICE extends the base series by taking the period-over-period difference in the splice series, and
         applying the difference to the base series.
        '''
        if base_series is None:
            logger.warning('No historical data for {} to level_splice, country {}, using country forecast '
                           'data.'.format(splice_series.name[1], splice_series.name[0]))
            return splice_series
        name = base_series.name
        result = None
        if kind == 'forward' or kind == 'both':
            stripped_base, stripped_splice, start_splice_loc = self._strip_and_get_forward_splice_boundaries(
                base_series, splice_series)
            if start_splice_loc is not None:
                diff = (stripped_splice.iloc[
                        start_splice_loc - 1:] - stripped_splice.iloc[start_splice_loc - 1:].shift(1))[1:]
                new_data = diff[1:].copy()
                new_data.iloc[0] = stripped_base.iloc[-1] + new_data.iloc[0]
                for index, item in list(diff.iteritems())[2:]:
                    new_data.loc[index] = new_data.loc[index - 1] + item
                result = pd.concat([stripped_base, new_data, splice_series.iloc[splice_series.index.get_loc(
                    stripped_splice.index[-1]) + 1:]], sort=True)
                result.name = name
            else:
                variable, country = 'unknown', 'unknown'
                if type(base_series.name) == tuple:
                    variable, country = base_series.name[1], base_series.name[0]
                logger.warning('Failed to splice {} forward, country {}, splice series ends before base series'.format(
                    variable, country))

        if kind == 'backward' or kind == 'both':
            stripped_base, stripped_splice, greater_splice_loc = self._strip_and_get_backward_splice_boundaries(
                base_series, splice_series)
            stripped_result = stripped_base
            if result is not None:
                stripped_result = result.iloc[result.index.get_loc(stripped_base.index[0]):]
            if greater_splice_loc is not None:
                diff = (stripped_splice.iloc[
                        :greater_splice_loc + 2] - stripped_splice.iloc[:greater_splice_loc + 2].shift(1))[:-1]
                new_data = diff[:-1].copy()
                new_data.iloc[-1] = stripped_base.iloc[0] - diff.iloc[-1]
                for index, item in list(reversed(list(diff.iteritems())))[1:-1]:
                    new_data.loc[index - 1] = new_data.loc[index] - item
                result = pd.concat([splice_series.iloc[:splice_series.index.get_loc(
                    stripped_splice.index[0])], new_data, stripped_result], sort=True)
                result.name = name
            else:
                variable, country = 'unknown', 'unknown'
                if type(base_series.name) == tuple:
                    variable, country = base_series.name[1], base_series.name[0]
                logger.warning('Failed to splice {} forward, country {}, splice series ends before base series'.format(
                    variable, country))

        return result

    def splice_and_level_forward(self, base_series, splice_series, kind='forward', variable=None, scales=None):
        '''
        SPLICE_AND_LEVEL performs the operation RatioSplice(base, level(series)) = base * (1 + 0,01 * series)
        '''
        # RatioSplice(base, level(series)) = base * (1 + 0,01 * series)
        # TODO: check if we need to implement backwards
        if base_series is None:
            logger.warning('No historical data for {} to splice_and_level, using country forecast '
                           'data.'.format(variable or 'Unknown variable'))
            return splice_series
        name = base_series.name
        result = None
        if kind == 'forward' or kind == 'both':
            stripped_base, stripped_splice, start_splice_loc = self._strip_and_get_forward_splice_boundaries(
                base_series, splice_series)
            if start_splice_loc is not None:
                new_data = stripped_splice.iloc[start_splice_loc - 1:][1:].copy()
                new_data.iloc[0] = stripped_base.iloc[-1]
                for index, item in list(new_data.iteritems())[1:]:
                    new_data.loc[index] = float(new_data.loc[index - 1]) * (1 + 0.01 * float(item))
                result = pd.concat([stripped_base, new_data[1:]], sort=True)
                result.name = name
            else:
                variable, country = 'unknown', 'unknown'
                if type(base_series.name) == tuple:
                    variable, country = base_series.name[1], base_series.name[0]
                logger.warning('Failed to splice {} forward, country {}, splice series ends before base series'.format(
                    variable, country))

        return result
