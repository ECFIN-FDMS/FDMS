#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pandas as pd

from fdms.helpers.splicer import Splicer


class TestSplice(unittest.TestCase):
    '''Tests for "Splice" functions.'''

    def setUp(self):
        self.base_dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='base_series1', index_col=[0, 2])
        self.splice_dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='test_splice1', index_col=[0, 1])

    def test_butt_splice(self):
        base_series = self.base_dataframe.loc[('BE', 'UTVTBP')].filter(regex='\d{4}')
        splice_series = self.splice_dataframe.loc[('BE', 'UTVTBP.1.0.0.0')].filter(regex='\d{4}')
        self.assertEqual(base_series.first_valid_index(), 2000)
        self.assertEqual(base_series.last_valid_index(), 2013)
        self.assertEqual(base_series.index[0], 1996)
        self.assertEqual(base_series.index[-1], 2020)
        self.assertEqual(splice_series.first_valid_index(), 1995)
        self.assertEqual(splice_series.last_valid_index(), 2023)
        self.assertEqual(splice_series.index[0], 1960)
        self.assertEqual(splice_series.index[-1], 2025)
        splicer = Splicer()
        result_backward = splicer.butt_splice(base_series, splice_series, kind='backward')
        self.assertEqual(result_backward.first_valid_index(), 1995)
        self.assertEqual(result_backward.last_valid_index(), 2013)
        self.assertEqual(result_backward.index[0], 1960)
        self.assertEqual(result_backward.index[-1], 2020)
        result_forward = splicer.butt_splice(base_series, splice_series, kind='forward')
        self.assertEqual(result_forward.first_valid_index(), 2000)
        self.assertEqual(result_forward.last_valid_index(), 2023)
        self.assertEqual(result_forward.index[0], 1996)
        self.assertEqual(result_forward.index[-1], 2025)
        result_both = splicer.butt_splice(base_series, splice_series, kind='both')
        self.assertEqual(result_both.first_valid_index(), 1995)
        self.assertEqual(result_both.last_valid_index(), 2023)
        self.assertEqual(result_both.index[0], 1960)
        self.assertEqual(result_both.index[-1], 2025)
