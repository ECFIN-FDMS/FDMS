import pandas as pd
import re

from fdms.config import BASE_PERIOD
from fdms.config.country_groups import EU, FCRIF
from fdms.utils.mixins import StepMixin
from fdms.utils.series import export_to_excel, get_scale
from fdms.utils.operators import Operators
from fdms.utils.splicer import Splicer


# STEP 11
class LabourMarket(StepMixin):
    def perform_computation(self, df, ameco_df):
        operators = Operators()
        splicer = Splicer()
        variables = ['FETD9.1.0.0.0', 'FWTD9.1.0.0.0']
        if self.country in FCRIF:
            try:
                fetd9 = self.get_data(df, 'FETD.1.0.0.0')
                fwtd9 = self.get_data(df, 'FWTD.1.0.0.0')
            except KeyError:
                fetd9 = self.get_data(df, 'NETD.1.0.0.0')
                fwtd9 = self.get_data(df, 'NWTD.1.0.0.0')
            series_meta = self.get_meta(variables[0])
            series_data = fetd9.copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
            series_meta = self.get_meta(variables[1])
            series_data = fwtd9.copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
        else:
            series_meta = self.get_meta(variables[0])
            if self.country == 'US':
                fetd9 = self.get_data(df, 'NETD.1.0.0.0')
                fwtd9 = self.get_data(df, 'NWTD.1.0.0.0')
            else:
                fetd9 = splicer.ratio_splice(self.get_data(ameco_df, variables[0]), self.get_data(
                    df, 'NETD'), kind='forward')
                fwtd9 = splicer.ratio_splice(self.get_data(ameco_df, variables[0]), self.get_data(
                    df, 'NWTD'), kind='forward')
            series_data = fetd9.copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
            series_meta = self.get_meta(variables[1])
            series_data = fwtd9.copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variables = ['UWCD', 'UWWD', 'UWSC']
        variables_1 = [variable + '.1.0.0.0' for variable in variables]
        variables_h1 = [re.sub('^U', 'H', variable) + 'W.1.0.0.0' for variable in variables]
        compensation = 'FWTD9.1.0.0.0'
        private_consumption_u = 'UCPH.1.0.0.0'
        private_consumption_o = 'OCPH.1.0.0.0'
        variables_r1 = [re.sub('^U', 'R', variable) + 'C.3.1.0.0' for variable in variables]
        services = ['UMSN', 'UXSN', 'UMSN.1.0.0.0', 'UXSN.1.0.0.0']
        for index, variable in enumerate(variables):
            series_meta = self.get_meta(variables_h1[index])
            series_data = self.get_data(df, variables_1[index]) / fwtd9
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

            series_meta = self.get_meta(variables_r1[index])
            series_data = operators.rebase(self.get_data(df, variables_1[index]) / fwtd9 / self.get_data(
                df, private_consumption_u) / self.get_data(df, private_consumption_o), base_period=BASE_PERIOD)
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variables = ['RVGDE.1.0.0.0', 'RVGEW.1.0.0.0', 'RVGEW.1.0.0.0', 'ZATN9.1.0.0.0', 'ZETN9.1.0.0.0',
                     'ZUTN9.1.0.0.0']
        numerators = ['OVGD.1.0.0.0', 'OVGE.1.0.0.0', 'OVGD.1.0.0.0', 'NLTN.1.0.0.0', 'NETN.1.0.0.0',
                      'NUTN.1.0.0.0']
        denominators = ['FETD9.1.0.0.0', 'FETD9.1.0.0.0', 'NETD.1.0.0.0', 'NPAN1.1.0.0.0', 'NPAN1.1.0.0.0',
                        'NLTN.1.0.0.0']
        for index, variable in enumerate(variables):
            series_meta = self.get_meta(variable)
            if denominators[index] == 'FETD9.1.0.0.0':
                denominator_series = fetd9
            else:
                denominator_series = self.get_data(df, denominators[index])
            series_data = self.get_data(df, numerators[index]) / denominator_series
            if variable in ['ZATN9.1.0.0.0', 'ZETN9.1.0.0.0', 'ZUTN9.1.0.0.0']:
                series_data = series_data * 100
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'FETD9.6.0.0.0'
        series_meta = self.get_meta(variable)
        series_data = fetd9.pct_change() * 100
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'ZUTN.1.0.0.0'
        if self.country in EU:
            # ZUTN based on NUTN.1.0.0.0 and NETN.1.0.0.0 (18/01/2017) is commented out in FDMS+
            last_observation = self.get_data(ameco_df, variable).last_valid_index()
            series_meta = self.get_meta(variable)
            series_data = round(self.get_data(df, 'NUTN') / (
                    self.get_data(df, 'NUTN') + self.get_data(df, 'NETN')) * 100, 1) + round(self.get_data(
                ameco_df, 'NUTN.1.0.0.0')[last_observation] - self.get_data(df, 'NUTN') / (self.get_data(
                df, 'NUTN')[last_observation] + self.get_data(df, 'NETN')[last_observation]), 1)
            series_data = splicer.butt_splice(self.get_data(ameco_df, variable), self.get_data(
                ameco_df, variable), kind='forward')
        else:
            try:
                netn1 = self.get_data(df, 'NETN.1.0.0.0')
            except KeyError:
                netn1 = self.get_data(df, 'NETN')
            series_data = splicer.level_splice(self.get_data(ameco_df, variable), self.get_data(
                df, 'NUTN.1.0.0.0') / (self.get_data(df, 'NUTN.1.0.0.0') + self.get_data(df, netn1)) * 100)

        # NUTN ratiospliced (18/01/2017) is commented out in FDMS+

        plcd3 = 'plcd3_series'
        variables = ['PLCD.3.1.0.0', 'QLCD.3.1.0.0']
        numerators = ['HWCDW.1.0.0.0', 'PLCD.3.1.0.0']
        denominators = ['RVGDE.1.0.0.0', 'PVGD.3.1.0.0']
        for index, variable in enumerate(variables):
            series_meta = self.get_meta(variable)
            if denominators[index] == 'PVGD.3.1.0.0':
                denominator_series = self.get_data(df, denominators[index])
            else:
                denominator_series = self.get_data(self.result, denominators[index])
            series_data = operators.rebase(self.get_data(self.result, numerators[
                index]) / denominator_series, base_period=BASE_PERIOD)
            if index == 0:
                plcd3 = series_data.copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variables = ['RWCDC.3.1.0.0', 'PLCD.3.1.0.0', 'QLCD.3.1.0.0', 'HWCDW.1.0.0.0', 'HWSCW.1.0.0.0', 'HWWDW.1.0.0.0',
                     'RVGDE.1.0.0.0', 'RVGEW.1.0.0.0']
        variables_6 = [re.sub('.....0.0$', '.6.0.0.0', variable) for variable in variables]
        for index, variable in enumerate(variables):
            series_meta = self.get_meta(variables_6[index])
            series_data = self.get_data(self.result, variable).pct_change() * 100
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, 'output/outputvars11.txt', 'output/output11.xlsx')
        return self.result
