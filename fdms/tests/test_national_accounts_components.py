import unittest
import pandas as pd

from fdms.computation.country.annual.transfer_matrix import TransferMatrix
from fdms.computation.country.annual.national_accounts_components import GDPComponents
from fdms.helpers.operators import read_country_forecast_excel, read_ameco_txt


class TestNationalAccountsVolume(unittest.TestCase):
    # National Accounts - Calculate additional GDP components
    # National Accounts (Value) - calculate additional components
    def setUp(self):
        self.country = 'BE'
        forecast_filename, ameco_filename = 'fdms/sample_data/BE.Forecast.0908.xlsm', 'fdms/sample_data/AMECO_H.TXT'
        self.df, self.ameco_df = read_country_forecast_excel(forecast_filename), read_ameco_txt(ameco_filename)
        self.expected_df = pd.read_excel('fdms/sample_data/BE_expected.xlsx', sheet_name='Table', index_col=[0, 2])

    def test_national_accounts_components(self):
        step_1 = TransferMatrix()
        result_1 = step_1.perform_computation(self.df, self.ameco_df)
        step_3 = GDPComponents()
        step_3_vars = ['UMGN', 'UMSN', 'UXGN', 'UXSN', 'UMGN', 'UMSN', 'UXGS', 'UMGS', 'UIGG0', 'UIGT', 'UIGG', 'UIGCO',
                       'UIGDW', 'UCPH', 'UCTG', 'UIGT', 'UIST']
        step_3_additional_vars = ['UMGN.1.0.0.0', 'UMSN.1.0.0.0', 'UXGN.1.0.0.0', 'UXSN.1.0.0.0', 'UMGN.1.0.0.0',
                                  'UMSN.1.0.0.0', 'UXGS.1.0.0.0', 'UMGS.1.0.0.0', 'UIGG0.1.0.0.0', 'UIGT.1.0.0.0',
                                  'UIGG.1.0.0.0', 'UIGCO.1.0.0.0', 'UIGDW.1.0.0.0', 'UCPH.1.0.0.0', 'UCTG.1.0.0.0',
                                  'UIGT.1.0.0.0', 'UIST.1.0.0.0', 'UXGN', 'UMGN']
        ameco_series = self.ameco_df.loc[self.ameco_df.index.isin(step_3_additional_vars, level='Variable Code')].copy()
        # step_3_df = result_1.append(ameco_series, sort=True)
        step_3_df = pd.concat([result_1, ameco_series], sort=True)
        result_3 = step_3.perform_computation(step_3_df)
        variables = ['UMGS', 'UXGS', 'UBGN', 'UBSN', 'UBGS', 'UIGG', 'UIGP', 'UIGNR', 'UUNF', 'UUNT', 'UUTT', 'UITT',
                     'UMGS.1.0.0.0', 'UXGS.1.0.0.0', 'UBGN.1.0.0.0', 'UBSN.1.0.0.0', 'UBGS.1.0.0.0', 'UIGG.1.0.0.0',
                     'UIGP.1.0.0.0', 'UIGNR.1.0.0.0', 'UUNF.1.0.0.0', 'UUNT.1.0.0.0', 'UUTT.1.0.0.0', 'UITT.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_3.loc['BE'].index)]
        print(missing_vars)
        self.assertFalse(missing_vars)

