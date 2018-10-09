import pandas as pd

from fdms.utils.series import COLUMN_ORDER, get_series_noindex


class StepMixin:
    country = 'BE'
    frequency = 'Annual'
    scale = 'units'

    def __init__(self, country=country, frequency=frequency, scale=scale):
        self.country = country
        self.frequency = frequency
        self.scale = scale
        self.result = pd.DataFrame(columns=COLUMN_ORDER)

    def update_result(self, series):
        series = self.result.loc[(self.result['Country Ameco'] == series['Country Ameco']) & (
            self.result['Variable Code'] == series['Variable Code'])]
        if series.empty:
            self.result.append(series, ignore_index=True, sort=True)
        else:
            self.result.iloc[series.index.values[0]] = series
