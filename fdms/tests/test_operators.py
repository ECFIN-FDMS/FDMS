#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pandas as pd
from pandas.testing import assert_series_equal

from fdms.helpers.operators import Operators


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