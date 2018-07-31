#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pandas as pd


class TestSplice(unittest.TestCase):
    '''Tests for "Splice" function.'''

    def setUp(self):
        self.data = pd.read_excel('fdms/tests/sample_data.xlsx', index_col=[0, 2])

    def test_butt_splice(self):
        series1 = self.data.loc[('BE', 'UTVTBP.1.0.0.0')].filter(regex='\d{4}')
        self.assertEqual(series1.first_valid_index(), 1995)
        self.assertEqual(series1.last_valid_index(), 2017)
        self.assertEqual(2, 2)

