import pandas as pd
import re

from fdms.config.variable_groups import NA_IS_VA
from fdms.utils.mixins import StepMixin
from fdms.utils.series import get_series, get_series_noindex, export_to_excel


# STEP 5
class NationalAccountsValue(StepMixin):
    def perform_computation(self, df, ovgd1):
        variables = ['UVGN.1.0.0.0', 'UTVNBP.1.0.0.0', 'UVGE.1.0.0.0', 'UWSC.1.0.0.0']
        component_1 = ['UVGD.1.0.0.0', 'UTVTBP.1.0.0.0', 'UVGD.1.0.0.0', 'UWCD.1.0.0.0']
        component_2 = ['UBRA.1.0.0.0', 'UYVTBP.1.0.0.0', 'UTVNBP.1.0.0.0', 'UWWD']
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'units'}
            if index == 0:
                series_data = get_series(df, self.country, component_1[index]) + get_series(
                    df, self.country, component_2[index])
            elif index == 1:
                series_data = get_series(df, self.country, component_1[index]) - get_series(
                    df, self.country, component_2[index])
                utvnbp = series_data.copy()
            elif index == 2:
                series_data = get_series(df, self.country, component_1[index]).subtract(utvnbp, fill_value=0)
            else:
                series_data = get_series(df, self.country, component_1[index]) - get_series(
                    df, self.country, component_2[index])
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
            # TODO: Check math
            # self.update_result(series)
            # if variable == 'UVGE.1.0.0.0':
            #     import code;code.interact(local=locals())

        variable = 'UOGD.1.0.0.0'
        components = ['UVGD.1.0.0.0', 'UYVG.1.0.0.0', 'UYEU.1.0.0.0', 'UWCD.1.0.0.0', 'UTVG.1.0.0.0', 'UTEU.1.0.0.0']
        series = [get_series(df, self.country, var) for var in components[:3]]
        series.extend([-get_series(df, self.country, var) for var in components[3:]])
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'units'}
        series_data = sum(series)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'UWCDA.1.0.0.0'
        total_employment = 'NETD.1.0.0.0'
        compensation = 'UWCD.1.0.0.0'
        real_compensation = 'NWTD.1.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'units'}
        series_data = (get_series(df, self.country, total_employment) * get_series(df, self.country, compensation) /
                       get_series(df, self.country, real_compensation))
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        for variable in NA_IS_VA:
            variable_1 = variable + '.1.0.0.0'
            variable_cc = re.sub('^U', 'CC', variable_1)
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable_cc, 'Frequency': 'Annual',
                           'Scale': 'units'}
            try:
                pch = get_series(df, self.country, variable_1) / ovgd1
            except KeyError:
                pch = get_series_noindex(self.result, self.country, variable_1) / ovgd1
            pch = pch.pct_change()
            try:
                series_data = get_series(df, self.country, variable_1) / get_series(
                    df, self.country, 'UVGD.1.0.0.0') * pch
            except KeyError:
                series_data = get_series_noindex(self.result, self.country, variable_1) / get_series(
                    df, self.country, 'UVGD.1.0.0.0') * pch
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_to_excel(self.result, 'output/outputvars5.txt', 'output/output5.xlsx')
        return self.result
