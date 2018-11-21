import unittest
import pandas as pd
import re

from pandas.testing import assert_series_equal

from fdms.computation.country.annual.labour_market import LabourMarket
from fdms.computation.country.annual.transfer_matrix import TransferMatrix
from fdms.computation.country.annual.population import Population
from fdms.computation.country.annual.national_accounts_components import GDPComponents
from fdms.computation.country.annual.national_accounts_volume import NationalAccountsVolume
from fdms.computation.country.annual.national_accounts_value import NationalAccountsValue
from fdms.computation.country.annual.recalculate_uvgdh import RecalculateUvgdh
from fdms.computation.country.annual.prices import Prices
from fdms.computation.country.annual.capital_stock import CapitalStock
from fdms.computation.country.annual.output_gap import OutputGap
from fdms.computation.country.annual.exchange_rates import ExchangeRates
from fdms.computation.country.annual.fiscal_sector import FiscalSector
from fdms.computation.country.annual.corporate_sector import CorporateSector
from fdms.computation.country.annual.household_sector import HouseholdSector
from fdms.config import YEARS
from fdms.config.scale_correction import fix_scales
from fdms.config.variable_groups import NA_VO, T_VO
from fdms.utils.interfaces import (
    read_country_forecast_excel, read_ameco_txt, read_expected_result_be, read_ameco_db_xls, read_output_gap_xls,
    read_xr_ir_xls, read_ameco_xne_us_xls, get_scales_from_forecast)
from fdms.utils.series import report_diff, remove_duplicates, export_to_excel


class TestCountryCalculations(unittest.TestCase):
    # National Accounts - Calculate additional GDP components
    # National Accounts (Value) - calculate additional components
    def setUp(self):
        self.country = 'BE'
        ameco_filename = 'fdms/sample_data/AMECO_H.TXT'
        forecast_filename = 'fdms/sample_data/{}.Forecast.SF2018.xlsm'.format(self.country)
        self.df, self.ameco_df = read_country_forecast_excel(forecast_filename), read_ameco_txt(ameco_filename)
        self.ameco_db_df = read_ameco_db_xls()
        self.ameco_db_df_all_data = read_ameco_db_xls(all_data=True)
        self.dfexp = read_expected_result_be()
        self.scales = get_scales_from_forecast(self.country)
        step_1 = TransferMatrix(scales=self.scales)
        self.result_1 = step_1.perform_computation(self.df, self.ameco_df)
        with open('errors_scale.txt', 'w') as f:
            pass
        with open('errors_scale.txt', 'w') as f:
            pass
        with open('raro.txt', 'a') as f:
            pass

    def _get_ameco_df(self, ameco_vars):
        ameco_series = self.ameco_df.loc[self.ameco_df.index.isin(ameco_vars, level='Variable Code')].copy().loc[
            self.country]
        ameco_df = pd.DataFrame(ameco_series)
        ameco_df.insert(0, 'Country Ameco', self.country)
        ameco_df = ameco_df.reset_index()
        ameco_df.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        return ameco_df

    def test_country_calculation_BE(self):
        # STEP 2
        step_2 = Population(scales=self.scales)
        step_2_vars = ['NUTN.1.0.0.0', 'NETN.1.0.0.0', 'NWTD.1.0.0.0', 'NETD.1.0.0.0', 'NPAN1.1.0.0.0', 'NETN',
                       'NLHA.1.0.0.0']
        # NECN.1.0.0.0 is calculated and used in step_2
        step_2_df = self.result_1.loc[self.result_1.index.isin(step_2_vars, level='Variable Code')].copy()
        result_2 = step_2.perform_computation(step_2_df, self.ameco_df)
        variables = ['NLTN.1.0.0.0', 'NETD.1.0.414.0', 'NECN.1.0.0.0', 'NLHT.1.0.0.0', 'NLHT9.1.0.0.0',
                     'NLCN.1.0.0.0', 'NSTD.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_2.loc[self.country].index)]
        self.assertFalse(missing_vars)

        # STEP 3
        step_3 = GDPComponents(scales=self.scales)
        step_3_vars = ['UMGN', 'UMSN', 'UXGN', 'UXSN', 'UMGN', 'UMSN', 'UXGS', 'UMGS', 'UIGG0', 'UIGT', 'UIGG', 'UIGCO',
                       'UIGDW', 'UCPH', 'UCTG', 'UIGT', 'UIST']
        step_3_additional_vars = ['UMGN.1.0.0.0', 'UMSN.1.0.0.0', 'UXGN.1.0.0.0', 'UXSN.1.0.0.0', 'UMGN.1.0.0.0',
                                  'UMSN.1.0.0.0', 'UXGS.1.0.0.0', 'UMGS.1.0.0.0', 'UIGG0.1.0.0.0', 'UIGT.1.0.0.0',
                                  'UIGG.1.0.0.0', 'UIGCO.1.0.0.0', 'UIGDW.1.0.0.0', 'UCPH.1.0.0.0', 'UCTG.1.0.0.0',
                                  'UIGT.1.0.0.0', 'UIST.1.0.0.0', 'UXGN', 'UMGN']
        result_3 = step_3.perform_computation(self.result_1, self.ameco_df)
        variables = ['UMGS', 'UXGS', 'UBGN', 'UBSN', 'UBGS', 'UIGG', 'UIGP', 'UIGNR', 'UUNF', 'UUNT', 'UUTT', 'UITT',
                     'UMGS.1.0.0.0', 'UXGS.1.0.0.0', 'UBGN.1.0.0.0', 'UBSN.1.0.0.0', 'UBGS.1.0.0.0', 'UIGG.1.0.0.0',
                     'UIGP.1.0.0.0', 'UIGNR.1.0.0.0', 'UUNF.1.0.0.0', 'UUNT.1.0.0.0', 'UUTT.1.0.0.0', 'UITT.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_3.loc[self.country].index)]
        self.assertFalse(missing_vars)

        # STEP 4
        step_4 = NationalAccountsVolume(scales=self.scales)

        # These variables have been calculated and are needed later
        calculated = ['UMGS', 'UXGS', 'UBGN', 'UBSN', 'UBGS', 'UIGG', 'UIGP', 'UIGNR', 'UUNF', 'UUNT', 'UUTT', 'UUITT']
        step_4_src_vars = list(NA_VO)
        step_4_src_vars.extend(calculated)
        step_4_src_vars.extend(['OMGS', 'OVGE', 'OVGD'])
        step_4_1000vars = [variable + '.1.0.0.0' for variable in step_4_src_vars]
        step_4_uvars = [re.sub('^.', 'U', variable) for variable in step_4_src_vars]
        step_4_1100vars = [variable + '.1.1.0.0' for variable in step_4_src_vars]

        # Per capita GDP: RVGDP.1.1.0.0
        step_4_1000vars.append('OVGD.1.0.0.0')
        step_4_1100vars.append('RVGDP.1.1.0.0')

        step_4_df = pd.concat([self.df, self.result_1, result_3], sort=True)
        # result_4, ovgd1 = step_4.perform_computation(step_4_df, ameco_df)
        result_4, ovgd1 = step_4.perform_computation(step_4_df, self.ameco_df)
        # missing_vars = [v for v in step_4_1000vars if v not in list(result_4.loc[self.country].index)]
        # self.assertFalse(missing_vars)

        # STEP 5
        step_5 = NationalAccountsValue(scales=self.scales)
        step_5_df = self.result_1.copy()
        result_5 = step_5.perform_computation(step_5_df, self.ameco_db_df, ovgd1)
        variables = ['UVGN.1.0.0.0', 'UVGN.1.0.0.0', 'UOGD.1.0.0.0', 'UOGD.1.0.0.0', 'UTVNBP.1.0.0.0', 'UTVNBP.1.0.0.0',
                     'UVGE.1.0.0.0', 'UVGE.1.0.0.0', 'UWCDA.1.0.0.0', 'UWCDA.1.0.0.0', 'UWSC.1.0.0.0', 'UWSC.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_5.loc[self.country].index)]
        self.assertFalse(missing_vars)

        PD = ['PCPH.3.1.0.0', 'PCTG.3.1.0.0', 'PIGT.3.1.0.0', 'PIGCO.3.1.0.0', 'PIGDW.3.1.0.0', 'PIGNR.3.1.0.0',
              'PIGEQ.3.1.0.0', 'PIGOT.3.1.0.0', 'PUNF.3.1.0.0', 'PUNT.3.1.0.0', 'PUTT.3.1.0.0', 'PVGD.3.1.0.0',
              'PXGS.3.1.0.0', 'PMGS.3.1.0.0', 'PXGN.3.1.0.0', 'PXSN.3.1.0.0', 'PMGN.3.1.0.0', 'PMSN.3.1.0.0',
              'PIGP.3.1.0.0', 'PIST.3.1.0.0', 'PVGE.3.1.0.0']

        PD_O = ['OCPH.1.0.0.0', 'OCTG.1.0.0.0', 'OIGT.1.0.0.0', 'OIGCO.1.0.0.0', 'OIGDW.1.0.0.0', 'OIGNR.1.0.0.0',
                'OIGEQ.1.0.0.0', 'OIGOT.1.0.0.0', 'OUNF.1.0.0.0', 'OUNT.1.0.0.0', 'OUTT.1.0.0.0', 'OVGD.1.0.0.0',
                'OXGS.1.0.0.0', 'OMGS.1.0.0.0', 'OXGN.1.0.0.0', 'OXSN.1.0.0.0', 'OMGN.1.0.0.0', 'OMSN.1.0.0.0',
                'OIGP.1.0.0.0', 'OIST.1.0.0.0', 'OVGE.1.0.0.0']

        PD_U = ['UCPH.1.0.0.0', 'UCTG.1.0.0.0', 'UIGT.1.0.0.0', 'UIGCO.1.0.0.0', 'UIGDW.1.0.0.0', 'UIGNR.1.0.0.0',
                'UIGEQ.1.0.0.0', 'UIGOT.1.0.0.0', 'UUNF.1.0.0.0', 'UUNT.1.0.0.0', 'UUTT.1.0.0.0', 'UVGD.1.0.0.0',
                'UXGS.1.0.0.0', 'UMGS.1.0.0.0', 'UXGN.1.0.0.0', 'UXSN.1.0.0.0', 'UMGN.1.0.0.0', 'UMSN.1.0.0.0',
                'UIGP.1.0.0.0', 'UIST.1.0.0.0', 'UVGE.1.0.0.0']

        # STEP 6
        ameco_vars = ['UVGDH.1.0.0.0', 'KNP.1.0.212.0']
        ameco_df = self._get_ameco_df(ameco_vars)
        step_6 = RecalculateUvgdh(scales=self.scales)
        result_6 = step_6.perform_computation(self.df, ameco_df)

        # STEP 7
        step_7 = Prices(scales=self.scales)
        step_7_df = pd.concat([self.result_1, result_3, result_4, result_5], sort=True)
        result_7 = step_7.perform_computation(step_7_df)
        variables = list(PD)
        missing_vars = [v for v in variables if v not in list(result_7.loc[self.country].index)]
        self.assertFalse(missing_vars)

        # STEP 8
        step_8 = CapitalStock(scales=self.scales)
        step_8_df = pd.concat([self.result_1, result_2, result_3, result_4, result_5], sort=True)
        result_8 = step_8.perform_computation(step_8_df, self.ameco_df, self.ameco_db_df_all_data)
        # variables = list(PD)
        # missing_vars = [v for v in variables if v not in list(result_8.loc[self.country].index)]
        # self.assertFalse(missing_vars)

        # STEP 9
        step_9 = OutputGap(scales=self.scales)
        result_9 = step_9.perform_computation(read_output_gap_xls())
        # variables = list(PD)
        # missing_vars = [v for v in variables if v not in list(result_9.loc[self.country].index)]
        # self.assertFalse(missing_vars)

        # STEP 10
        step_10 = ExchangeRates(scales=self.scales)
        result_10 = step_10.perform_computation(self.ameco_db_df, read_xr_ir_xls(), read_ameco_xne_us_xls())
        # variables = list(PD)
        # missing_vars = [v for v in variables if v not in list(result_10.loc[self.country].index)]
        # self.assertFalse(missing_vars)

        # STEP 11
        step_11 = LabourMarket(scales=self.scales)
        step_11_df = pd.concat([self.result_1, result_2, result_4, result_5, result_7], sort=True)
        result_11 = step_11.perform_computation(step_11_df, self.ameco_df)
        variables = ['FETD9.1.0.0.0', 'FWTD9.1.0.0.0', 'HWCDW.1.0.0.0', 'RWCDC.3.1.0.0', 'HWWDW.1.0.0.0',
                     'RWWDC.3.1.0.0', 'HWSCW.1.0.0.0', 'RWSCC.3.1.0.0', 'RVGDE.1.0.0.0', 'RVGEW.1.0.0.0',
                     'RVGEW.1.0.0.0', 'ZATN9.1.0.0.0', 'ZETN9.1.0.0.0', 'ZUTN9.1.0.0.0', 'FETD9.6.0.0.0',
                     'PLCD.3.1.0.0', 'QLCD.3.1.0.0', 'RWCDC.6.0.0.0', 'PLCD.6.0.0.0', 'QLCD.6.0.0.0', 'HWCDW.6.0.0.0',
                     'HWSCW.6.0.0.0', 'HWWDW.6.0.0.0', 'RVGDE.6.0.0.0', 'RVGEW.6.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_11.loc[self.country].index)]
        self.assertFalse(missing_vars)

        # STEP 12
        step_12 = FiscalSector()
        result_12 = step_12.perform_computation(self.result_1, self.ameco_df)
        # variables = list(PD)
        # missing_vars = [v for v in variables if v not in list(result_12.loc[self.country].index)]
        # self.assertFalse(missing_vars)

        # STEP 13
        step_13 = CorporateSector(scales=self.scales)
        result_13 = step_13.perform_computation(self.result_1, self.ameco_df)
        variables = ['USGC.1.0.0.0', 'UOGC.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_13.loc[self.country].index)]
        self.assertFalse(missing_vars)

        # STEP 14
        step_14 = HouseholdSector(scales=self.scales)
        result_14 = step_14.perform_computation(self.result_1, result_7, self.ameco_df)
        variables = ['UYOH.1.0.0.0', 'UVGH.1.0.0.0', 'UVGHA.1.0.0.0', 'OVGHA.3.0.0.0', 'USGH.1.0.0.0', 'ASGH.1.0.0.0',
                     'UBLH.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_14.loc[self.country].index)]
        self.assertFalse(missing_vars)

        # TODO: Fix all scales
        result = pd.concat([self.result_1, result_2, result_3, result_4, result_5, result_6, result_7, result_8,
                            result_9, result_10, result_11, result_12, result_13, result_14], sort=True)
        result = remove_duplicates(result)
        fix_scales(result, self.country)
        export_to_excel(result, 'output/outputall.txt', 'output/outputall.xlsx')

        # res = result.drop(columns=['Scale'])
        res = result.copy()
        # res.loc[:, YEARS] = res.loc[:, YEARS].round(decimals=4)
        columns = res.columns
        rows = result.index.tolist()
        self.dfexp['Frequency'] = 'Annual'
        exp = self.dfexp[columns].reindex(rows)
        # exp.loc[:, YEARS] = exp.loc[:, YEARS].round(decimals=4)
        diff = (exp == res) | (exp != exp) & (res != res)
        diff_series = diff.all(axis=1)
        wrong_series = []
        for i in range(1, res.shape[0]):
            try:
                assert_series_equal(res.iloc[i], exp.iloc[i])
            except AssertionError:
                wrong_series.append(res.iloc[i])
        wrong_names = [series.name for series in wrong_series]
        res_wrong, exp_wrong = res.loc[wrong_names].copy(), exp.loc[wrong_names].copy()
        report_diff(res_wrong, exp_wrong)
