#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pandas as pd
import numpy as np
from pandas.testing import assert_series_equal

from fdms.helpers.splicer import Splicer
from fdms.helpers.operators import get_series
from fdms.config.country_groups import *
from fdms.config.variable_groups import *


class TestSplice(unittest.TestCase):
    '''Tests for "Splice" functions'''

    def setUp(self):
        self.base_dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='base_series1', index_col=[0, 2])
        self.splice_dataframe = pd.read_excel(
            'fdms/tests/sample_data.xlsx', sheet_name='ameco1', index_col=[0, 1])
        self.quarterly_dataframe = pd.read_excel(
            'fdms/tests/sample_data.xlsx', sheet_name='quarterly_series', index_col=[0, 2])
        self.bad_index_dataframe = pd.read_excel(
            'fdms/tests/sample_data.xlsx', sheet_name='empty_series', index_col=[0, 2])

    def test_butt_splice(self):
        base_series = get_series(self.base_dataframe, 'BE', 'UTVTBP')
        splice_series = get_series(self.splice_dataframe, 'BE', 'UTVTBP.1.0.0.0')
        name = base_series.name

        base_series_data = [np.nan] * 4 + [
            714520000, np.nan, np.nan, 999350000, 1187470000, 1364510000, 1726780000, 2072000000,
            1894140000, 1965010000, 1934920000, 2150610000, 2366150000, 2417210000
        ] + [np.nan] * 7
        base_series_index = pd.Index([x for x in range(1996, 2021)], dtype='object')
        splice_series_data = [np.nan] * 35 + [
            22.746, 23.991, 25.374, 26.329, 28.177, 29.687, 29.276, 30.505, 31.298, 33.625,
            35.67, 37.241, 39.244, 39.414, 38.092, 40.912, 41.972, 42.977, 43.548, 44.175,
            45.094, 47.52389796, 49.8012431, 51.71180553, 54.06542708, 56.27850325, 58.49157943,
            60.7046556, 62.91773177, np.nan, np.nan]
        splice_series_index = pd.Index([x for x in range(1960, 2026)], dtype='object')

        expected_base_series = pd.Series(base_series_data, index=base_series_index, dtype='object',
                                         name=name)
        expected_splice_series = pd.Series(splice_series_data, index=splice_series_index, dtype='object',
                                           name=splice_series.name)
        expected_backward_data = splice_series_data[:40] + base_series_data[4:]
        expected_forward_data = base_series_data[:18] + splice_series_data[54:]
        expected_both_data = splice_series_data[:40] + base_series_data[4:18] + splice_series_data[54:]
        expected_backward_index = pd.Index([x for x in range(1960, 2021)])
        expected_forward_index = pd.Index([x for x in range(1996, 2026)])
        expected_both_index = pd.Index([x for x in range(1960, 2026)])
        expected_backward_series = pd.Series(
            expected_backward_data, index=expected_backward_index, dtype='object', name=name)
        expected_forward_series = pd.Series(
            expected_forward_data, index=expected_forward_index, dtype='object', name=name)
        expected_both_series = pd.Series(
            expected_both_data, index=expected_both_index, dtype='object', name=name)

        assert_series_equal(base_series, expected_base_series)
        assert_series_equal(splice_series, expected_splice_series)

        splicer = Splicer()
        result_backward = splicer.butt_splice(base_series, splice_series, kind='backward')
        result_forward = splicer.butt_splice(base_series, splice_series, kind='forward')
        result_both = splicer.butt_splice(base_series, splice_series, kind='both')

        assert_series_equal(result_backward, expected_backward_series)
        assert_series_equal(result_forward, expected_forward_series)
        assert_series_equal(result_both, expected_both_series)

    def test_quarterly_and_empty_series(self):
        quarterly_series = get_series(self.quarterly_dataframe, 'BE', 'UTVTBP')
        empty_series = get_series(self.bad_index_dataframe, 'BE', 'UTVTBP')
        self.assertEqual(len(quarterly_series), 16)
        self.assertIsNone(empty_series)

    def test_splice_series_short_is_logged(self):
        base_series = get_series(self.base_dataframe, 'BE', 'UTVTBP')
        splice_series = get_series(self.splice_dataframe, 'BE', 'UTVTBP.1.0.0.0')
        short_splice_start = splice_series.index.get_loc(base_series.first_valid_index())
        short_splice_end = splice_series.index.get_loc(base_series.last_valid_index() + 1)
        short_splice_series1 = splice_series.iloc[short_splice_start:short_splice_end]
        short_splice_series2 = splice_series.iloc[short_splice_start + 2:short_splice_end - 10]
        splicer = Splicer()
        msg = ('WARNING:fdms.helpers.splicer:Failed to splice UTVTBP forward, country BE, splice series ends before '
               'base series')
        with self.assertLogs() as logs:
            result_both1 = splicer.butt_splice(base_series, short_splice_series1, kind='both')
            result_both2 = splicer.butt_splice(base_series, short_splice_series2, kind='both')
        self.assertIn(msg, logs.output)
        self.assertEqual(len(logs.output), 4)

    def test_ratio_splice(self):
        dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='ratiosplice', index_col=3)
        base_series = dataframe.loc['base_series'].filter(regex='\d{4}')
        splice_series = dataframe.loc['splice_series'].filter(regex='\d{4}')
        expected_result = dataframe.loc['ratio_splice'].filter(regex='\d{4}')

        splicer = Splicer()
        # result_backward = splicer.ratio_splice(base_series, splice_series, kind='backward')
        # result_forward = splicer.butt_splice(base_series, splice_series, kind='forward')
        result_both = splicer.ratio_splice(base_series, splice_series, kind='both')
        result_both.name = expected_result.name
        result_both.index = pd.Index(result_both.index, dtype='object')
        assert_series_equal(result_both, expected_result)

        # assert_series_equal(result_backward, expected_backward_series)
        # assert_series_equal(result_forward, expected_forward_series)
        # assert_series_equal(result_both, expected_result)
        # TODO: Add more tests for ratio_splice

    def test_ratio_splice_series_short_is_logged(self):
        dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='ratiosplice', index_col=3)
        base_series = dataframe.loc['base_series'].filter(regex='\d{4}')
        splice_series = dataframe.loc['splice_series'].filter(regex='\d{4}')
        base_series = get_series(self.base_dataframe, 'BE', 'UTVTBP')
        splice_series = get_series(self.splice_dataframe, 'BE', 'UTVTBP.1.0.0.0')
        short_splice_start = splice_series.index.get_loc(base_series.first_valid_index())
        short_splice_end = splice_series.index.get_loc(base_series.last_valid_index() + 1)
        short_splice_series1 = splice_series.iloc[short_splice_start:short_splice_end]
        short_splice_series2 = splice_series.iloc[short_splice_start + 2:short_splice_end - 10]
        splicer = Splicer()
        with self.assertLogs() as logs:
            result_both1 = splicer.ratio_splice(base_series, short_splice_series1, kind='both')
            result_both2 = splicer.ratio_splice(base_series, short_splice_series2, kind='both')
        self.assertEqual(len(logs.output), 4)

    def test_level_splice(self):
        dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='levelsplice', index_col=3)
        base_series = dataframe.loc['base_series'].filter(regex='\d{4}')
        splice_series = dataframe.loc['splice_series'].filter(regex='\d{4}')
        expected_result = dataframe.loc['level_splice'].filter(regex='\d{4}')

        splicer = Splicer()
        # result_backward = splicer.ratio_splice(base_series, splice_series, kind='backward')
        # result_forward = splicer.butt_splice(base_series, splice_series, kind='forward')
        result_both = splicer.level_splice(base_series, splice_series, kind='both')
        result_both.name = expected_result.name
        result_both.index = pd.Index(result_both.index, dtype='object')
        assert_series_equal(result_both, expected_result)

    def test_level_splice_series_short_is_logged(self):
        dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='ratiosplice', index_col=3)
        base_series = dataframe.loc['base_series'].filter(regex='\d{4}')
        splice_series = dataframe.loc['splice_series'].filter(regex='\d{4}')
        base_series = get_series(self.base_dataframe, 'BE', 'UTVTBP')
        splice_series = get_series(self.splice_dataframe, 'BE', 'UTVTBP.1.0.0.0')
        short_splice_start = splice_series.index.get_loc(base_series.first_valid_index())
        short_splice_end = splice_series.index.get_loc(base_series.last_valid_index() + 1)
        short_splice_series1 = splice_series.iloc[short_splice_start:short_splice_end]
        short_splice_series2 = splice_series.iloc[short_splice_start + 2:short_splice_end - 10]
        splicer = Splicer()
        with self.assertLogs() as logs:
            result_both1 = splicer.level_splice(base_series, short_splice_series1, kind='both')
            result_both2 = splicer.level_splice(base_series, short_splice_series2, kind='both')
        self.assertEqual(len(logs.output), 4)
       # TODO: Add more tests for level_splice
