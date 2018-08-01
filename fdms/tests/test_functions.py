#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pandas as pd
import numpy as np
from pandas.testing import assert_series_equal

from fdms.helpers.splicer import get_series, Splicer


class TestSplice(unittest.TestCase):
    '''Tests for "Splice" functions'''

    def setUp(self):
        self.base_dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='base_series1', index_col=[0, 2])
        self.splice_dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='test_splice1', index_col=[0, 1])

    def test_butt_splice(self):
        base_series = get_series(self.base_dataframe, 'BE', 'UTVTBP')
        splice_series = get_series(self.splice_dataframe, 'BE', 'UTVTBP.1.0.0.0')
        name = base_series.name

        base_series_data = [np.nan] * 4 + [
            714520000, 808580000, 918200000, 999350000, 1187470000, 1364510000, 1726780000, 2072000000,
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
