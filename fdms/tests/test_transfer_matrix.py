import unittest
import pandas as pd

from fdms.helpers.operators import get_series
from fdms.helpers.splicer import Splicer
from fdms.computation.country.annual.transfer_matrix import TransferMatrix
from fdms.helpers.operators import read_raw_data


class TestTransferMatrix(unittest.TestCase):
    # Convert all transfer matrix variables to 1.0.0.0 (except National Account (volume)) and splice in
    # country desk forecast
    def setUp(self):
        pass
        # self.country = 'BE'
        # self.df, self.ameco_df = read_raw_data('fdms/sample_data/BE.Forecast.0908.xlsm',
        #                                        'fdms/sample_data/BE_AMECO.xlsx', 'BE',)
        # self.expected_df = pd.read_excel('fdms/sample_data/BE.raw.0908.xlsx', sheet_name='result-spring2018',
        #                                  index_col=[2, 3])

    def test_to_be_buttspliced_only(self):
        pass
        # step_1 = TransferMatrix()
        # result_1 = step_1.perform_computation(self.df, self.ameco_df)

    def test_to_be_merged(self):
        pass
        # expected_result = get_series(self.expected_df, self.country, new_variable)
        # base_series = get_series(self.ameco_df, self.country, ameco_variable)
        # splice_series = get_series(self.df, self.country, variable) / (
        #         get_series(self.df, self.country, related_variable).shift(1) - 1) * 100

    def test_the_rest(self):
        pass