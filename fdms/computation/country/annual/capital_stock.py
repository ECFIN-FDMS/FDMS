import pandas as pd

from fdms.utils.mixins import StepMixin
from fdms.utils.series import get_series, get_series_noindex, export_to_excel
from fdms.utils.splicer import Splicer
from fdms.config import FIRST_YEAR, LAST_YEAR


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

        series_1 = get_series(df, self.country, 'OVGD.1.0.0.0')
        series_2 = get_series(df, self.country, 'OIGT.1.0.0.0')

        # TODO: Check the math in FDMS+, these ones are really strange
        if series_1.first_valid_index() + 1 < series_2.first_valid_index():
            last_observation = series_2.first_valid_index() - 1
        else:
            last_observation = series_1.first_valid_index()
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        new_series = pd.Series(series_meta)
        oint_1 = get_series_noindex(self.result, self.country, 'OINT.1.0.0.0').copy()
        oigt_1 = get_series_noindex(self.result, self.country, 'OIGT.1.0.0.0').copy()
        new_data = pd.Series({year: pd.np.nan for year in range(FIRST_YEAR, LAST_YEAR + 1)})
        new_data[last_observation] = 3 * oint_1[last_observation]
        for year in range(last_observation + 1, LAST_YEAR):
            new_data[year] = new_data[year - 1] + oint_1[year]
        last_observation = self.result[self.result['Variable Code'] == 'OKCT.1.0.0.0'].iloc[-1].last_valid_index()
        # TODO: Review the math, some results seem wrong
        for year in range(last_observation + 1, LAST_YEAR + 1):
            self.result.loc[
                self.result['Variable Code'] == 'OKCT.1.0.0.0', [year]] = (new_data[year - 1] * self.result.loc[
                self.result['Variable Code'] == 'OKCT.1.0.0.0', [year - 1]] / new_data[year - 2]).iloc[0, 0]

            new_data[year] = (new_data[year - 1] + oigt_1[year] - self.result.loc[
                self.result['Variable Code'] == 'OKCT.1.0.0.0', [year]]).iloc[0, 0]

            self.result.loc[
                self.result['Variable Code'] == 'OINT.1.0.0.0', [year]] = (oigt_1[year] - self.result.loc[
                self.result['Variable Code'] == 'OKCT.1.0.0.0', [year]]).iloc[0, 0]

            self.result.loc[
                self.result['Variable Code'] == 'UKCT.1.0.0.0', [year]] = (self.result.loc[
                self.result['Variable Code'] == 'OKCT.1.0.0.0', [year]] * get_series_noindex(
                self.result, self.country, 'UIGT.1.0.0.0')[year] / oigt_1[year]).iloc[0, 0]

        new_series = new_series.append(new_data)
        self.result = self.result.append(new_series, ignore_index=True, sort=True)

        variable = 'ZVGDFA3.3.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        series_3 = get_series(df, self.country, 'NLHT9.1.0.0.0')
        series_data = pd.np.log(series_1 / (pow(series_3 * 1000, 0.65) * pow(new_data, 0.35)))
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_to_excel(self.result, 'output/outputvars8.txt', 'output/output8.xlsx')
        return self.result
