import unittest
import pandas as pd

from fdms.helpers.operators import get_series
from fdms.helpers.splicer import Splicer
from fdms.computation.country.annual.transfer_matrix import TransferMatrix
from fdms.computation.country.annual.national_accounts_components import GDPComponents
from fdms.helpers.operators import read_raw_data


class TestNationalAccountsVolume(unittest.TestCase):
    # National Accounts - Calculate additional GDP components
    # National Accounts (Value) - calculate additional components
    def setUp(self):
        self.country = 'BE'
        self.df, self.ameco_df = read_raw_data('fdms/sample_data/BE.Forecast.0908.xlsm',
                                               'fdms/sample_data/BE_AMECO.xlsx', 'BE',)
        self.expected_df = pd.read_excel('fdms/sample_data/BE.raw.0908.xlsx', sheet_name='result-spring2018',
                                         index_col=[2, 3])

    def test_national_accounts_components(self):
        step_1 = TransferMatrix()
        result_1 = step_1.perform_computation(self.df, self.ameco_df)
        step_3 = GDPComponents()
        result_3 = step_3.perform_computation(result_1)
        variables = ['UMGS', 'UXGS', 'UBGN', 'UBSN', 'UBGS', 'UIGG', 'UIGP', 'UIGNR', 'UUNF', 'UUNT', 'UUTT', 'UITT',
                     'UMGS.1.0.0.0', 'UXGS.1.0.0.0', 'UBGN.1.0.0.0', 'UBSN.1.0.0.0', 'UBGS.1.0.0.0', 'UIGG.1.0.0.0',
                     'UIGP.1.0.0.0', 'UIGNR.1.0.0.0', 'UUNF.1.0.0.0', 'UUNT.1.0.0.0', 'UUTT.1.0.0.0', 'UITT.1.0.0.0']
        # TODO: There are four variables missing: ['UBGS', 'UIGP', 'UBGS.1.0.0.0', 'UIGP.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_3.loc['BE'].index)]
        print(missing_vars)
        self.assertEqual(missing_vars, ['UBGS', 'UIGP', 'UBGS.1.0.0.0', 'UIGP.1.0.0.0'])


