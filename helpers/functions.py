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
        :param splice_series:
        :type splice_series: pandas.core.frame.DataFrame
        :param str method:
        :param str kind:
        :param bool overlap:
        :param bool replace_empty_base_series:
        :param period:
        :return:
        :rtype: pandas.core.frame.DataFrame
        '''
