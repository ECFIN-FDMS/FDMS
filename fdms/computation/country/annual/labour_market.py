import pandas as pd
import re

from fdms.config import BASE_PERIOD
from fdms.config.country_groups import EU, FCRIF
from fdms.utils.mixins import StepMixin
from fdms.utils.series import get_series, get_series_noindex, export_to_excel, get_scale
from fdms.utils.operators import Operators
from fdms.utils.splicer import Splicer


class LabourMarket(StepMixin):
    def perform_computation(self, df, ameco_df):
        operators = Operators()
        splicer = Splicer()
        variables = ['FETD9.1.0.0.0', 'FWTD9.1.0.0.0']
        if self.country in FCRIF:
            try:
                fetd9 = get_series(df, self.country, 'FETD.1.0.0.0')
                fwtd9 = get_series(df, self.country, 'FWTD.1.0.0.0')
            except KeyError:
                fetd9 = get_series(df, self.country, 'NETD.1.0.0.0')
                fwtd9 = get_series(df, self.country, 'NWTD.1.0.0.0')
            series_meta = {'Country Ameco': self.country, 'Variable Code': variables[0], 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = fetd9.copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
            series_meta = {'Country Ameco': self.country, 'Variable Code': variables[1], 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = fwtd9.copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
        else:
            series_meta = {'Country Ameco': self.country, 'Variable Code': variables[0], 'Frequency': 'Annual',
                           'Scale': 'billions'}
            if self.country == 'US':
                fetd9 = get_series(df, self.country, 'NETD.1.0.0.0')
                fwtd9 = get_series(df, self.country, 'NWTD.1.0.0.0')
            else:
                fetd9 = splicer.ratio_splice(get_series(ameco_df, self.country, variables[0]), get_series(
                    df, self.country, 'NETD'), kind='forward')
                fwtd9 = splicer.ratio_splice(get_series(ameco_df, self.country, variables[0]), get_series(
                    df, self.country, 'NWTD'), kind='forward')
            series_data = fetd9.copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
            series_meta = {'Country Ameco': self.country, 'Variable Code': variables[1], 'Frequency': 'Annual',
                           'Scale': 'billions'}
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
            series_meta = {'Country Ameco': self.country, 'Variable Code': variables_h1[index], 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = get_series(df, self.country, variables_1[index]) / fwtd9
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

            series_meta = {'Country Ameco': self.country, 'Variable Code': variables_r1[index], 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = operators.rebase(get_series(df, self.country, variables_1[index]) / fwtd9 / get_series(
                df, self.country, private_consumption_u) / get_series(df, self.country, private_consumption_o),
                                           base_period=BASE_PERIOD)
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
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            if denominators[index] == 'FETD9.1.0.0.0':
                denominator_series = fetd9
            else:
                denominator_series = get_series(df, self.country, denominators[index])
            series_data = get_series(df, self.country, numerators[index]) / denominator_series
            if variable in ['ZATN9.1.0.0.0', 'ZETN9.1.0.0.0', 'ZUTN9.1.0.0.0']:
                series_data = series_data * 100
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'FETD9.6.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'units'}
        series_data = fetd9.pct_change()
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'ZUTN.1.0.0.0'
        if self.country in EU:
            # ZUTN based on NUTN.1.0.0.0 and NETN.1.0.0.0 (18/01/2017) is commented out in FDMS+
            last_observation = get_series(ameco_df, self.country, variable).last_valid_index()
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = round(get_series(df, self.country, 'NUTN') / (get_series(
                df, self.country, 'NUTN') + get_series(df, self.country, 'NETN')) * 100, 1) + round(get_series(
                ameco_df, self.country, 'NUTN.1.0.0.0')[last_observation] - get_series(df, self.country, 'NUTN') / (
                get_series(df, self.country, 'NUTN')[last_observation] + get_series(df, self.country, 'NETN')[
                last_observation]), 1)
            series_data = splicer.butt_splice(get_series(ameco_df, self.country, variable), get_series(
                ameco_df, self.country, variable), kind='forward')
        else:
            try:
                netn1 = get_series(df, self.country, 'NETN.1.0.0.0')
            except KeyError:
                netn1 = get_series(df, self.country, 'NETN')
            series_data = splicer.level_splice(get_series(ameco_df, self.country, variable), get_series(
                df, self.country, 'NUTN.1.0.0.0') / (get_series(df, self.country, 'NUTN.1.0.0.0') + get_series(
                df, self.country, netn1)) * 100)

        # NUTN ratiospliced (18/01/2017) is commented out in FDMS+

        plcd3 = 'plcd3_series'
        variables = ['PLCD.3.1.0.0', 'QLCD.3.1.0.0']
        numerators = ['HWCDW.1.0.0.0', 'PLCD.3.1.0.0']
        denominators = ['RVGDE.1.0.0.0', 'PVGD.3.1.0.0']
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            if denominators[index] == 'PVGD.3.1.0.0':
                denominator_series = get_series(df, self.country, denominators[index])
            else:
                denominator_series = get_series_noindex(self.result, self.country, denominators[index])
            series_data = operators.rebase(get_series_noindex(self.result, self.country, numerators[
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
            series_meta = {'Country Ameco': self.country, 'Variable Code': variables_6[index], 'Frequency': 'Annual',
                           'Scale': 'units'}
            series_data = get_series_noindex(self.result, self.country, variable).pct_change()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_to_excel(self.result, 'output/outputvars10.txt', 'output/output10.xlsx')
        return self.result
