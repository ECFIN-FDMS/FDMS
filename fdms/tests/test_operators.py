#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pandas as pd
from pandas.testing import assert_series_equal

from fdms.helpers.operators import Operators, get_series


class TestOperators(unittest.TestCase):
    '''Tests for "Splice" functions'''

    def setUp(self):
        pass

    def test_merge(self):
        dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='merge', index_col=0)
        expected = dataframe.loc['expected'].filter(regex='\d{4}')
        calc = Operators()
        result = calc.merge(dataframe)
        result.name = 'expected'
        assert_series_equal(result, expected)

    def test_iin(self):
        dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='iin', index_col=[0, 2])
        src = get_series(dataframe, 'BE', 'UTVTBP')
        new_data = get_series(dataframe, 'BE', 'new_data')
        expected = get_series(dataframe, 'BE', 'expected')
        calc = Operators()
        result = calc.iin(src, new_data, src / 1000000)
        result.name = ('BE', 'expected')
        assert_series_equal(result, expected)

    def test_pch(self):
        dataframe = pd.read_excel('fdms/tests/sample_data.xlsx', sheet_name='iin', index_col=[0, 2])
        src = get_series(dataframe, 'BE', 'UTVTBP')
        calc = Operators()
        result = calc.pch(src)
        assert_series_equal(result, src.pct_change() * 100)
