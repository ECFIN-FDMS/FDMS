import re

import pandas as pd

from fdms.utils.mixins import StepMixin
from fdms.config.variable_groups import PD
from fdms.utils.operators import Operators
from fdms.utils.series import get_series, get_series_noindex, export_to_excel, get_scale
from fdms.utils.splicer import Splicer
from fdms.config import LAST_YEAR


# STEP 8
class CapitalStock(StepMixin):
    def perform_computation(self, df, ameco_df, ameco_db_df):
        '''Capital Stock and Total Factor Productivity'''
        variables = ['OIGT.1.0.0.0', 'OVGD.1.0.0.0', 'UIGT.1.0.0.0']
        splicer = Splicer()
        for variable in variables:
            try:
                series_data = get_series(df, self.country, variable)
            except KeyError:
                # TODO: log
                continue
            if series_data is not None:
                series_data = splicer.ratio_splice(series_data, get_series(ameco_db_df, self.country, variable),
                                                   kind='backward', variable=variable)
                series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                               'Scale': 'billions'}
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

        # TODO: Fix this one... AMECO seems old?
        variable = 'UKCT.1.0.0.0'
        try:
            ameco_data = get_series(ameco_df, self.country, variable)
        except KeyError:
            series_data = get_series(ameco_db_df, self.country, variable)
        else:
            series_data = splicer.ratio_splice(ameco_data, get_series(ameco_db_df, self.country, variable),
                                               kind='backward')
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'OKCT.1.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        series_data = get_series_noindex(self.result, self.country, 'UKCT.1.0.0.0') / get_series(
            df, self.country, 'UIGT.1.0.0.0') / get_series(df, self.country, 'OIGT.1.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        variable = 'OINT.1.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        series_data = get_series(df, self.country, 'OIGT.1.0.0.0') - get_series_noindex(
            self.result, self.country, 'OKCT.1.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'OKND.1.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        new_series = pd.Series({year: 0 for year in self.result.columns.tolist()})

        series_1 = get_series(df, self.country, 'OVGD.1.0.0.0')  # .first_valid_index() + 1
        series_2 = get_series(df, self.country, 'OIGT.1.0.0.0')  # .first_valid_index()
        if series_1.first_valid_index() + 1 < series_2.first_valid_index():
            last_observation = series_2.first_valid_index() - 1
        else:
            last_observation = series_1.first_valid_index()
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        try:
            new_series.update(get_series(df, self.country, 'OKND.1.0.0.0').shift(1) + get_series_noindex(
                self.result, self.country, 'OINT.1.0.0.0'))
        except KeyError:
            new_series.update(new_series.shift(1) + get_series_noindex(self.result, self.country, 'OINT.1.0.0.0'))
        new_series.update(pd.Series(series_meta))
        new_series[last_observation] = series_1[last_observation] * 3

        last_observation = self.result[self.result['Variable Code'] == 'OKCT.1.0.0.0'].iloc[-1].last_valid_index()
        date_range = list(range(last_observation, LAST_YEAR))
        series_3 = new_series.copy()
        self.result[self.result['Variable Code'] == 'OKCT.1.0.0.0'].update((series_3.filter(regex='\d{4}').shift(
            1) * self.result[self.result['Variable Code'] == 'OKCT.1.0.0.0'].filter(regex='\d{4}').shift(
            1, axis=1) / series_3.filter(regex='\d{4}').shift(2))[date_range])

        # TODO: Check the math in FDMS+, these ones are really strange
        # import code;code.interact(local=locals())
        # new_series = new_series.copy().shift(1) + get_series(df, self.country, 'OIGT.1.0.0.0') - get_series_noindex(
        #     self.result, self.country, 'OKCT.1.0.0.0')
        # self.result = self.result.append(new_series, ignore_index=True, sort=True)
        # variable = 'OKCT.1.0.0.0'
        # variable = 'OKND.1.0.0.0'
        # variable = 'OINR.1.0.0.0'
        # variable = 'UKCT.1.0.0.0'
        #
        # variable = 'ZVGDFA3.3.0.0.0'
