import pandas as pd

from fdms.config.scale_correction import SCALES
from fdms.utils.series import COLUMN_ORDER
from fdms.utils.splicer import Splicer


class StepMixin:
    country = 'BE'
    frequency = 'Annual'
    scale = 'Units'
    codes = {'Units': 0, 'Thousands': 1, 'Millions': 2, 'Billions': 3, '-': 0}

    def __init__(self, country=country, frequency=frequency, scale=scale, scales={}):
        self.country = country
        self.frequency = frequency
        self.scale = scale
        self.scales = scales
        self.scale_correction = {}
        self.result = pd.DataFrame(columns=COLUMN_ORDER)

    def update_result(self, series):
        series = self.result.loc[(self.result['Country Ameco'] == series['Country Ameco']) & (
            self.result['Variable Code'] == series['Variable Code'])]
        if series.empty:
            self.result.append(series, ignore_index=True, sort=True)
        else:
            self.result.iloc[series.index.values[0]] = series

    def get_scale(self, variable, dataframe=None, country=None):
        if dataframe is not None:
            country = self.country if country is None else country
            try:
                return dataframe.loc[(country, variable)]['Scale']
            except KeyError:
                pass

        expected = SCALES.get(variable)
        input_data = self.scales.get(variable)
        if expected:
            if input_data != expected:
                if variable not in self.scale_correction:
                    self.scale_correction[variable] = (input_data, expected)
                with open('errors_scale.txt', 'a') as f:
                    f.write(' '.join([variable, expected or '-', input_data or '-', '\n']))
        return (SCALES.get(variable) or self.scales.get(variable) or self.scale).capitalize()

    def apply_scale(self):
        for variable in self.scale_correction:
            meta = pd.Series(self.get_meta(variable))
            try:
                series = self.get_data(self.result, variable)
            except KeyError:
                return
            orig, expected = self.scale_correction[variable]
            if all([x is not None for x in [orig, expected]]):
                series = series * pow(1000, self.codes[orig] - self.codes[expected])
            try:
                self.result.loc[self.country, variable] = pd.concat([meta, series])
            except:
                with open('raro.txt', 'a') as f:
                    f.write(variable + '\n')

    def get_meta(self, variable):
        return {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': self.frequency,
                'Scale': self.get_scale(variable)}

    def get_data(self, dataframe, variable, country=None, null_dates=None):
        '''Get quarterly or yearly data from dataframe (input with MultiIndex or result with RangeIndex)'''
        country = self.country if country is None else country
        if type(dataframe.index) == pd.MultiIndex:
            dataframe.sort_index(level=[0, 1], inplace=True)
            series = dataframe.loc[(country, variable)].filter(regex='\d{4}')
            if series.empty:
                series = dataframe.loc[(country, variable)].filter(regex='\d{4}Q[1234]')
            if series.empty:
                return None
            # TODO: Log these and make sure that this is correct, check values and get the best one
            if len(series.shape) > 1:
                series = series.iloc[-1]
            series = pd.to_numeric(series.squeeze(), errors='coerce')
            if null_dates is not None:
                for year in null_dates:
                    series[year] = pd.np.nan
            return series

        elif type(dataframe.index) == pd.RangeIndex:
            result_series_index = dataframe.loc[(dataframe['Country Ameco'] == country) & (
                    dataframe['Variable Code'] == variable)].index.values[0]
            series = dataframe.loc[result_series_index]
            series = series.filter(regex='\d{4}')
            if series.empty:
                series = dataframe.loc[result_series_index].filter(regex='\d{4}Q[1234]')
            if series.empty:
                return None
            if len(series.shape) > 1:
                series = series.iloc[0]
            series = pd.to_numeric(series.squeeze(), errors='coerce')
            if null_dates is not None:
                for year in null_dates:
                    series[year] = pd.np.nan
            return series

    def get_index(self, variable_code, dataframe=None, country=None):
        dataframe = self.result if dataframe is None else dataframe
        country = self.country if country is None else country
        return dataframe.loc[(dataframe['Country Ameco'] == country) & (
                dataframe['Variable Code'] == variable_code)].index.values[0]


class SumAndSpliceMixin(StepMixin):
    def _sum_and_splice(self, addends, df, ameco_h_df, splice=True):
        splicer = Splicer()
        for variable, sources in addends.items():
            series_meta = self.get_meta(variable)
            expected_scale = series_meta.get('Scale')
            try:
                base_series = self.get_data(ameco_h_df, variable)
            except KeyError:
                base_series = None
            splice_series = pd.Series()
            for source in sources:
                factor = 1
                if source.startswith('-'):
                    source = source[1:]
                    factor = -1
                src_scale = self.get_scale(source, dataframe=df)
                expected_scale = self.get_scale(variable)
                if src_scale != expected_scale:
                    factor = factor * pow(1000, self.codes[src_scale] - self.codes[expected_scale])
                try:
                    source_data = factor * self.get_data(df, source)
                except KeyError:
                    source_data = factor * self.get_data(self.result, source)
                splice_series = splice_series.add(source_data, fill_value=0)

            if base_series is None or splice is False:
                series_data = splice_series
            else:
                series_data = splicer.butt_splice(base_series, splice_series, kind='forward')
            if self.country == 'JP' and variable in ['UUTG.1.0.0.0', 'URTG.1.0.0.0']:
                if variable == 'URTG.1.0.0.0':
                    new_sources = ['UUTG.1.0.0.0', 'UBLG.1.0.0.0']
                    splice_series = self.get_data(
                        self.result, new_sources[0]) + self.get_data(
                        self.result, new_sources[1]
                    )
                series_data = splicer.ratio_splice(base_series, splice_series, kind='forward')
            series_data = series_data
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
