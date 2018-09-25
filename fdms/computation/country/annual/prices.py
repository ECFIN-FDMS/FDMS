import pandas as pd
import re

from fdms.config.variable_groups import PD
from fdms.utils.series import get_series, get_series_noindex, export_to_excel
from fdms.utils.operators import Operators


BASE_PERIOD = 2010


class Prices:
    result = pd.DataFrame()
    country = 'BE'
    frequency = 'Annual'

    def perform_computation(self, df):
        '''splice AMECO Historical data with forecast data and calculate percent change, and GNI (GDP deflator)'''
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

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_to_excel(self.result, 'output/outputvars7.txt', 'output/output7.xlsx')
        return self.result
