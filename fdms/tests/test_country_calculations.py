import unittest
import pandas as pd
import re

from fdms.computation.country.annual.transfer_matrix import TransferMatrix
from fdms.computation.country.annual.population import Population
from fdms.computation.country.annual.national_accounts_components import GDPComponents
from fdms.computation.country.annual.national_accounts_volume import NationalAccountsVolume
from fdms.config.variable_groups import NA_VO
from fdms.helpers.operators import read_country_forecast_excel, read_ameco_txt


class TestCountryCalculations(unittest.TestCase):
    # National Accounts - Calculate additional GDP components
    # National Accounts (Value) - calculate additional components
    def setUp(self):
        self.country = 'BE'
        forecast_filename, ameco_filename = 'fdms/sample_data/LT.Forecast.SF2018.xlsm', 'fdms/sample_data/AMECO_H.TXT'
        self.df, self.ameco_df = read_country_forecast_excel(forecast_filename), read_ameco_txt(ameco_filename)
        self.expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        step_1 = TransferMatrix()
        self.result_1 = step_1.perform_computation(self.df, self.ameco_df)

    def test_transfer_matrix(self):
        pass

    def test_population(self):
        step_2 = Population()
        step_2_vars = ['NUTN.1.0.0.0', 'NETN.1.0.0.0', 'NWTD.1.0.0.0', 'NETD.1.0.0.0', 'NPAN1.1.0.0.0', 'NETN',
                       'NLHA.1.0.0.0']
        # NECN.1.0.0.0 is calculated and used in step_2
        step_2_df = self.result_1.loc[self.result_1.index.isin(step_2_vars, level='Variable Code')].copy()
        result_2 = step_2.perform_computation(step_2_df, self.ameco_df)
        variables = ['NLTN.1.0.0.0', 'NETD.1.0.414.0', 'NECN.1.0.0.0', 'NLHT.1.0.0.0', 'NLHT9.1.0.0.0',
                     'NLCN.1.0.0.0']  # 'NSTD.1.0.0.0' is missing in ameco_df
        missing_vars = [v for v in variables if v not in list(result_2.loc['BE'].index)]
        self.assertEqual(missing_vars, ['NLCN.1.0.0.0'])

    def test_national_accounts_components(self):
        step_3 = GDPComponents()
        step_3_vars = ['UMGN', 'UMSN', 'UXGN', 'UXSN', 'UMGN', 'UMSN', 'UXGS', 'UMGS', 'UIGG0', 'UIGT', 'UIGG', 'UIGCO',
                       'UIGDW', 'UCPH', 'UCTG', 'UIGT', 'UIST']
        step_3_additional_vars = ['UMGN.1.0.0.0', 'UMSN.1.0.0.0', 'UXGN.1.0.0.0', 'UXSN.1.0.0.0', 'UMGN.1.0.0.0',
                                  'UMSN.1.0.0.0', 'UXGS.1.0.0.0', 'UMGS.1.0.0.0', 'UIGG0.1.0.0.0', 'UIGT.1.0.0.0',
                                  'UIGG.1.0.0.0', 'UIGCO.1.0.0.0', 'UIGDW.1.0.0.0', 'UCPH.1.0.0.0', 'UCTG.1.0.0.0',
                                  'UIGT.1.0.0.0', 'UIST.1.0.0.0', 'UXGN', 'UMGN']
        ameco_series = self.ameco_df.loc[self.ameco_df.index.isin(step_3_additional_vars, level='Variable Code')].copy()
        step_3_df = pd.concat([self.result_1, ameco_series], sort=True)
        result_3 = step_3.perform_computation(step_3_df)
        variables = ['UMGS', 'UXGS', 'UBGN', 'UBSN', 'UBGS', 'UIGG', 'UIGP', 'UIGNR', 'UUNF', 'UUNT', 'UUTT', 'UITT',
                     'UMGS.1.0.0.0', 'UXGS.1.0.0.0', 'UBGN.1.0.0.0', 'UBSN.1.0.0.0', 'UBGS.1.0.0.0', 'UIGG.1.0.0.0',
                     'UIGP.1.0.0.0', 'UIGNR.1.0.0.0', 'UUNF.1.0.0.0', 'UUNT.1.0.0.0', 'UUTT.1.0.0.0', 'UITT.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_3.loc['BE'].index)]
        self.assertFalse(missing_vars)

    def test_national_accounts_volume(self):
        step_4 = NationalAccountsVolume()

        step_4_src_vars = list(NA_VO)
        step_4_1000vars = [variable + '.1.0.0.0' for variable in step_4_src_vars]
        step_4_uvars = [re.sub('^.', 'U', variable) for variable in step_4_src_vars]
        step_4_1100vars = [variable + '.1.1.0.0' for variable in step_4_src_vars]
        ameco_series = self.ameco_df.loc[self.ameco_df.index.isin(step_4_1100vars, level='Variable Code')].copy().loc[
            'BE']
        ameco_df = pd.DataFrame(ameco_series)
        ameco_df.insert(0, 'Country Ameco', 'BE')
        ameco_df = ameco_df.reset_index()
        ameco_df.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        step_4_df = pd.concat([ameco_df, self.result_1], sort=True)
        result_4 = step_4.perform_computation(step_4_df, ameco_series)
        # missing_vars = [v for v in step_4_1000vars if v not in list(result_4.loc['BE'].index)]
        # self.assertFalse(missing_vars)

