import re

import pandas as pd

from fdms.utils.mixins import StepMixin
from fdms.config.variable_groups import PD
from fdms.utils.operators import Operators
from fdms.utils.series import get_series, get_series_noindex, export_to_excel, get_scale
from fdms.utils.splicer import Splicer


class CapitalStock(StepMixin):
    def perform_computation(self, df, ameco_df):
        '''Capital Stock and Total Factor Productivity'''
        variables = ['OIGT.1.0.0.0', 'OVGD.1.0.0.0', 'UIGT.1.0.0.0']
        splicer = Splicer()
        for variable in variables:
            try:
                series_data = get_series(df, self.country, variable)
            except KeyError:
                continue
        if series_data is not None:
            series_data = splicer.ratio_splice(series_data, get_series(ameco_df, self.country, variable),
                                               kind='backward')
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'UKCT.1.0.0.0'
        try:
            ameco_data = get_series(ameco_df, self.country, variable)
        except KeyError:
            pass
        else:
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = splicer.ratio_splice(ameco_data, get_series(df, self.country, variable))
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'OKND.1.0.0.0'
        variable = 'OKND.1.0.0.0'
        series_1 = get_series(df, self.country, 'OVGD.1.0.0.0').first_valid_index + 1
        series_2 = get_series(df, self.country, 'OIGT.1.0.0.0').first_valid_index
        if series_1.first_valid_index() < series_2.first_valid_index():
            last_observation = series_2.first_valid_index() - 1
        else:
            last_observation = series_1.first_valid_index()

        variable = 'OKCD.1.0.0.0'
        src = 'OVGD.1.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        series_data = get_series(df, self.country, src) * 3
        variable = 'OKND.1.0.0.0'
        variable = 'OINT.1.0.0.0'
        variable = 'UKCT.1.0.0.0'

        variable = 'OKCT.1.0.0.0'
        variable = 'OKND.1.0.0.0'
        variable = 'OINT.1.0.0.0'
        variable = 'UKCT.1.0.0.0'

        variable = 'OKCT.1.0.0.0'
        variable = 'OKND.1.0.0.0'
        variable = 'OINR.1.0.0.0'
        variable = 'UKCT.1.0.0.0'

        variable = 'OKCT.1.0.0.0'
        variable = 'OKND.1.0.0.0'
        variable = 'OINR.1.0.0.0'
        variable = 'UKCT.1.0.0.0'

        variable = 'ZVGDFA3.3.0.0.0'

        zcpih, zcpih_6, zcpin = 'ZCPIH', 'ZCPIH.6.0.0.0', 'ZCPIN'
        series_meta = get_series(df, self.country, zcpin, metadata=True)
        series_meta['Variable Code'] = zcpih_6
        try:
            series_data = get_series(df, self.country, zcpih)
        except KeyError:
            series_data = get_series(df, self.country, zcpin)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        operators = Operators()
        for variable in PD:
            variable_u1 = re.sub('^P', 'U', re.sub('.3.1.0.0', '.1.0.0.0', variable))
            variable_o1 = re.sub('^P', 'O', re.sub('.3.1.0.0', '.1.0.0.0', variable))
            series_meta = get_series(df, self.country, variable_o1, metadata=True)
            series_meta['Variable Code'] = variable
            series_data = operators.rebase(get_series(df, self.country, variable_u1) / get_series(
                df, self.country, variable_o1), BASE_PERIOD, bp1=True)
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        # GNI (GDP deflator)
        variable = 'OVGN.1.0.0.0'
        variable_6 = 'OVGN.6.0.0.0'
        gross_income = 'UVGN.1.0.0.0'
        gross_domestic_product = 'PVGD.3.1.0.0'
        series_meta = {'Frequency': self.frequency, 'Scale': get_scale(df, self.country, gross_income),
                       'Country Ameco': self.country, 'Variable Code': variable}
        series_data = get_series(df, self.country, gross_income) / get_series_noindex(
            self.result, self.country, gross_domestic_product) * 100
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        series_meta = {'Frequency': self.frequency, 'Scale': get_scale(df, self.country, gross_income),
                       'Country Ameco': self.country, 'Variable Code': variable_6}
        series_data = series_data.copy().pct_change()
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_to_excel(self.result, 'output/outputvars7.txt', 'output/output7.xlsx')
        return self.result
