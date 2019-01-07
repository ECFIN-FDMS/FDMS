import unittest
import pandas as pd
import re

from pandas.testing import assert_series_equal
from fdms.config.variable_groups import NA_VO,TM,TM_TBBO,TM_TBM
from fdms.computation.country.annual.labour_market import LabourMarket
from fdms.computation.country.annual.transfer_matrix import TransferMatrix
from fdms.computation.country.annual.population import Population
from fdms.computation.country.annual.national_accounts_components import GDPComponents
from fdms.computation.country.annual.national_accounts_volume import NationalAccountsVolume
from fdms.computation.country.annual.national_accounts_value import NationalAccountsValue
from fdms.computation.country.annual.recalculate_uvgdh import RecalculateUvgdh
from fdms.computation.country.annual.prices import Prices
from fdms.computation.country.annual.output_gap import OutputGap
from fdms.config.variable_groups import NA_VO
from fdms.utils.interfaces import (read_country_forecast_excel, read_ameco_txt, read_expected_result_be,
                                   read_ameco_db_xls, read_output_gap_xls, read_xr_ir_xls)
from fdms.utils.series import get_series, report_diff, remove_duplicates
from fdms.computation.comparator import compare

class TestCountryCalculations(unittest.TestCase):
    # National Accounts - Calculate additional GDP components
    # National Accounts (Value) - calculate additional components
    def setUp(self):
        self.country = 'BE'
        forecast_filename, ameco_filename = 'fdms/sample_data/LT.Forecast.SF2018.xlsm', 'fdms/sample_data/AMECO_H.TXT'
        self.df, self.ameco_df = read_country_forecast_excel(forecast_filename), read_ameco_txt(ameco_filename)
        self.ameco_db_df = read_ameco_db_xls()
        #self.dfexp = read_expected_result_be()

        writer_vars = pd.ExcelWriter('output/Variables.xlsx')
        navo_df = pd.DataFrame(NA_VO)
        tm_df = pd.DataFrame(TM)
        tbbo_df = pd.DataFrame(TM_TBBO)
        tbm_df = pd.DataFrame(TM_TBM)
        navo_df.to_excel(writer_vars,'NA_VO')
        tm_df.to_excel(writer_vars,'TM')
        tbbo_df.to_excel(writer_vars,'TM_TBBO')
        tbm_df.to_excel(writer_vars, 'TM_TBM')

    def _get_ameco_df(self, ameco_vars):
        ameco_series = self.ameco_df.loc[self.ameco_df.index.isin(ameco_vars, level='Variable Code')].copy().loc[
            'BE']
        ameco_df = pd.DataFrame(ameco_series)
        ameco_df.insert(0, 'Country Ameco', 'BE')
        ameco_df = ameco_df.reset_index()
        ameco_df.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        return ameco_df

    def test_country_calculation_BE(self):

        # STEP 1
        step_1 = TransferMatrix()
        self.result_1 = step_1.perform_computation(self.df, self.ameco_df)
        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        expected_vars = pd.read_excel('fdms/sample_data/TM_expected_vars.xlsx')['Variable Code'].tolist()
        result = self.result_1
        filename = 'output/Test1.xlsx'
        differences1, wrong_vars1, additional_vars1 = compare(expected_df, expected_vars, result, filename)
        differences1.to_csv(path_or_buf='output/Test1.csv')
        #assert wrong_vars1 == []

        # STEP 2
        step_2 = Population()
        step_2_vars = ['NUTN.1.0.0.0', 'NETN.1.0.0.0', 'NWTD.1.0.0.0', 'NETD.1.0.0.0', 'NPAN1.1.0.0.0', 'NETN',
                       'NLHA.1.0.0.0']
        # NECN.1.0.0.0 is calculated and used in step_2
        step_2_df = self.result_1.loc[self.result_1.index.isin(step_2_vars, level='Variable Code')].copy()
        result_2 = step_2.perform_computation(step_2_df, self.ameco_df)
        variables = ['NLTN.1.0.0.0', 'NETD.1.0.414.0', 'NECN.1.0.0.0', 'NLHT.1.0.0.0', 'NLHT9.1.0.0.0',
                     'NLCN.1.0.0.0', 'NSTD.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_2.loc['BE'].index)]
        self.assertFalse(missing_vars)

        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        expected_vars = variables
        result = result_2
        filename = 'output/Test2.xlsx'
        differences2, wrong_vars2, additional_vars2 = self.comparator(expected_df, expected_vars, result, filename)
        differences2.to_csv(path_or_buf='output/Test2.csv')
        #assert wrong_vars2 == []

        # STEP 3
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

        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        expected_vars = variables
        result = result_3
        filename = 'output/Test3.xlsx'
        differences3, wrong_vars3, additional_vars3 = self.comparator(expected_df, expected_vars, result, filename)
        differences3.to_csv(path_or_buf='output/Test3.csv')
        #assert wrong_vars3 == []

        # STEP 4
        step_4 = NationalAccountsVolume()

        # These variables have been calculated and are needed later
        calculated = ['UMGS', 'UXGS', 'UBGN', 'UBSN', 'UBGS', 'UIGG', 'UIGP', 'UIGNR', 'UUNF', 'UUNT', 'UUTT', 'UUITT']
        step_4_src_vars = list(NA_VO)
        step_4_src_vars.extend(calculated)
        step_4_1000vars = [variable + '.1.0.0.0' for variable in step_4_src_vars]
        step_4_uvars = [re.sub('^.', 'U', variable) for variable in step_4_src_vars]
        step_4_1100vars = [variable + '.1.1.0.0' for variable in step_4_src_vars]

        # Per capita GDP: RVGDP.1.1.0.0
        step_4_1000vars.append('OVGD.1.0.0.0')
        step_4_1100vars.append('RVGDP.1.1.0.0')

        orig_series = self.df.loc[self.df.index.isin(step_4_src_vars, level='Variable')].copy().loc['BE']
        orig_series = pd.concat([orig_series, result_3.loc[result_3.index.isin(
            step_4_uvars, level='Variable Code')].copy().loc['BE']], sort=True)
        orig_series = pd.concat([orig_series, result_3.loc[result_3.index.isin(
            variables, level='Variable Code')].copy().loc['BE']], sort=True)
        orig_series['Variable Code'] = orig_series.index
        orig_series.insert(0, 'Country Ameco', 'BE')
        orig_series = orig_series.reset_index()
        orig_series.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        ameco_df = self._get_ameco_df(step_4_1100vars)
        step_4_df = self.result_1.copy()
        step_4_df = pd.concat([step_4_df, orig_series], sort=True)
        result_4 = step_4.perform_computation(step_4_df, ameco_df)
        # missing_vars = [v for v in step_4_1000vars if v not in list(result_4.loc['BE'].index)]
        # self.assertFalse(missing_vars)

        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        expected_vars = variables
        result = result_4
        filename = 'output/Test4.xlsx'
        writer = pd.ExcelWriter(filename)
        result.to_excel(writer, 'Results')
        expected_df.to_excel(writer, 'Expected')

        #differences4, wrong_vars4, additional_vars4 = self.comparator(expected_df, expected_vars, result, filename)
        #differences4.to_csv(path_or_buf='output/Test4.csv')
        #assert wrong_vars4 == []

        # STEP 5
        step_5 = NationalAccountsValue()
        step_5_df = self.result_1.copy()
        ovgd1 = get_series(result_4, 'BE', 'OVGD.1.0.0.0')
        result_5 = step_5.perform_computation(step_5_df, ovgd1)
        variables = ['UVGN.1.0.0.0', 'UVGN.1.0.0.0', 'UOGD.1.0.0.0', 'UOGD.1.0.0.0', 'UTVNBP.1.0.0.0', 'UTVNBP.1.0.0.0',
                     'UVGE.1.0.0.0', 'UVGE.1.0.0.0', 'UWCDA.1.0.0.0', 'UWCDA.1.0.0.0', 'UWSC.1.0.0.0', 'UWSC.1.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_5.loc['BE'].index)]
        self.assertFalse(missing_vars)

        PD = ['PCPH.3.1.0.0', 'PCTG.3.1.0.0', 'PIGT.3.1.0.0', 'PIGCO.3.1.0.0', 'PIGDW.3.1.0.0', 'PIGNR.3.1.0.0',
              'PIGEQ.3.1.0.0', 'PIGOT.3.1.0.0', 'PUNF.3.1.0.0', 'PUNT.3.1.0.0', 'PUTT.3.1.0.0', 'PVGD.3.1.0.0', 'PXGS.3.1.0.0',
              'PMGS.3.1.0.0', 'PXGN.3.1.0.0', 'PXSN.3.1.0.0', 'PMGN.3.1.0.0', 'PMSN.3.1.0.0', 'PIGP.3.1.0.0', 'PIST.3.1.0.0',
              'PVGE.3.1.0.0']

        PD_O = ['OCPH.1.0.0.0', 'OCTG.1.0.0.0', 'OIGT.1.0.0.0', 'OIGCO.1.0.0.0', 'OIGDW.1.0.0.0', 'OIGNR.1.0.0.0',
                'OIGEQ.1.0.0.0', 'OIGOT.1.0.0.0', 'OUNF.1.0.0.0', 'OUNT.1.0.0.0', 'OUTT.1.0.0.0', 'OVGD.1.0.0.0', 'OXGS.1.0.0.0',
                'OMGS.1.0.0.0', 'OXGN.1.0.0.0', 'OXSN.1.0.0.0', 'OMGN.1.0.0.0', 'OMSN.1.0.0.0', 'OIGP.1.0.0.0', 'OIST.1.0.0.0',
                'OVGE.1.0.0.0']

        PD_U = ['UCPH.1.0.0.0', 'UCTG.1.0.0.0', 'UIGT.1.0.0.0', 'UIGCO.1.0.0.0', 'UIGDW.1.0.0.0', 'UIGNR.1.0.0.0',
                'UIGEQ.1.0.0.0', 'UIGOT.1.0.0.0', 'UUNF.1.0.0.0', 'UUNT.1.0.0.0', 'UUTT.1.0.0.0', 'UVGD.1.0.0.0', 'UXGS.1.0.0.0',
                'UMGS.1.0.0.0', 'UXGN.1.0.0.0', 'UXSN.1.0.0.0', 'UMGN.1.0.0.0', 'UMSN.1.0.0.0', 'UIGP.1.0.0.0', 'UIST.1.0.0.0',
                'UVGE.1.0.0.0']

        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        expected_vars = variables
        result = result_5
        filename = 'output/Test5.xlsx'
        differences5, wrong_vars5, additional_vars5 = self.comparator(expected_df, expected_vars, result, filename)
        differences5.to_csv(path_or_buf='output/Test5.csv')
        #assert wrong_vars5 == []

        # STEP 6
        ameco_vars = ['UVGDH.1.0.0.0', 'KNP.1.0.212.0']
        ameco_df = self._get_ameco_df(ameco_vars)
        step_6 = RecalculateUvgdh()
        result_6 = step_6.perform_computation(self.df, ameco_df)

        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        expected_vars = ameco_vars
        result = result_6
        filename = 'output/Test6.xlsx'
        differences6, wrong_vars6, additional_vars6 = self.comparator(expected_df, expected_vars, result, filename)
        differences6.to_csv(path_or_buf='output/Test6.csv')
        # assert wrong_vars6 == []

        # STEP 7
        step_7 = Prices()
        step_7_df = pd.concat([self.result_1, result_3, result_4, result_5], sort=True)
        result_7 = step_7.perform_computation(step_7_df)
        variables = list(PD)
        missing_vars = [v for v in variables if v not in list(result_7.loc['BE'].index)]
        self.assertFalse(missing_vars)

        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        expected_vars = variables
        result = result_7
        filename = 'output/Test7.xlsx'
        differences7, wrong_vars7, additional_vars7 = self.comparator(expected_df, expected_vars, result, filename)
        differences7.to_csv(path_or_buf='output/Test7.csv')
        # assert wrong_vars7 == []

        # STEP 8
        #step_8 = CapitalStock()
        #step_8_df = pd.concat([self.result_1, result_3, result_4, result_5], sort=True)
        #result_8 = step_8.perform_computation(step_8_df, self.ameco_df, self.ameco_db_df)
        #variables = list(PD)
        #missing_vars = [v for v in variables if v not in list(result_8.loc['BE'].index)]
        #self.assertFalse(missing_vars)


        # STEP 9
        step_9 = OutputGap()
        result_9 = step_9.perform_computation(read_output_gap_xls())
        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        result = result_9
        filename = 'output/Test9.xlsx'
        writer = pd.ExcelWriter(filename)
        result.to_excel(writer, 'Results')
        expected_df.to_excel(writer, 'Expected')



        # STEP 10

        step_10 = ExchangeRates()
        result_10 = step_10.perform_computation(self.ameco_db_df, read_xr_ir_xls(), read_ameco_xne_us_xls())
        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        result = result_10
        filename = 'output/Test10.xlsx'
        writer = pd.ExcelWriter(filename)
        result.to_excel(writer, 'Results')
        expected_df.to_excel(writer, 'Expected')

        import pdb;
        pdb.set_trace()

        # STEP 11
        step_11 = LabourMarket()
        step_11_df = pd.concat([self.result_1, result_2, result_4, result_5, result_7], sort=True)  # , result_4, result_5])
        result_11 = step_11.perform_computation(step_11_df, self.ameco_df)
        variables = ['FETD9.1.0.0.0', 'FWTD9.1.0.0.0', 'HWCDW.1.0.0.0', 'RWCDC.3.1.0.0', 'HWWDW.1.0.0.0',
                     'RWWDC.3.1.0.0', 'HWSCW.1.0.0.0', 'RWSCC.3.1.0.0', 'RVGDE.1.0.0.0', 'RVGEW.1.0.0.0',
                     'RVGEW.1.0.0.0', 'ZATN9.1.0.0.0', 'ZETN9.1.0.0.0', 'ZUTN9.1.0.0.0', 'FETD9.6.0.0.0',
                     'PLCD.3.1.0.0', 'QLCD.3.1.0.0', 'RWCDC.6.0.0.0', 'PLCD.6.0.0.0', 'QLCD.6.0.0.0', 'HWCDW.6.0.0.0',
                     'HWSCW.6.0.0.0', 'HWWDW.6.0.0.0', 'RVGDE.6.0.0.0', 'RVGEW.6.0.0.0']
        missing_vars = [v for v in variables if v not in list(result_11.loc['BE'].index)]
        self.assertFalse(missing_vars)

        expected_df = pd.read_excel('fdms/sample_data/BE.exp.xlsx', sheet_name='Table', index_col=[1, 2])
        expected_vars = variables
        result = result_11
        filename = 'output/Test11.xlsx'
        #differences11, wrong_vars11, additional_vars11 = self.comparator(expected_df, expected_vars, result, filename)
        #differences11.to_csv(path_or_buf='output/Test11.csv')
        # assert wrong_vars11 == []

        result = pd.concat([self.result_1, result_2, result_3, result_4, result_5, result_6, result_7, result_11],
                           sort=True)
        result = remove_duplicates(result)

        # TODO: Fix all scales
        res = result.drop(columns=['Scale'])
        columns = res.columns
        rows = result.index.tolist()
        self.dfexp['Frequency'] = 'Annual'
        exp = self.dfexp[columns].loc[rows]
        diff = (exp == res) | (exp != exp) & (res != res)
        diff_series = diff.all(axis=1)
        wrong_series = []
        for i in range(1, res.shape[0]):
            try:
                assert_series_equal(res.iloc[i], exp.iloc[i])
            except AssertionError:
                wrong_series.append(res.iloc[i])
        # report_diff(res, exp, diff, diff_series)
        wrong_names = [series.name for series in wrong_series]
        res_wrong, exp_wrong = res.loc[wrong_names].copy(), exp.loc[wrong_names].copy()
        report_diff(res_wrong, exp_wrong)