import pandas as pd
import re

from fdms.config import BASE_PERIOD
from fdms.config.variable_groups import PD
from fdms.utils.mixins import StepMixin
from fdms.utils.series import export_to_excel
from fdms.utils.operators import Operators


# STEP 7
class Prices(StepMixin):
    def perform_computation(self, df):
        '''splice AMECO Historical data with forecast data and calculate percent change, and GNI (GDP deflator)'''
        zcpih, zcpih_6, zcpin = 'ZCPIH', 'ZCPIH.6.0.0.0', 'ZCPIN'
        # series_meta = self.get_meta(zcpin)
        # series_meta['Variable Code'] = zcpih_6
        series_meta = self.get_meta(zcpih_6)
        try:
            series_data = self.get_data(df, zcpih)
        except KeyError:
            series_data = self.get_data(df, zcpin)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        operators = Operators()
        for variable in PD:
            variable_u1 = re.sub('^P', 'U', re.sub('.3.1.0.0', '.1.0.0.0', variable))
            variable_o1 = re.sub('^P', 'O', re.sub('.3.1.0.0', '.1.0.0.0', variable))
            # series_meta = self.get_meta(variable_o1)
            # series_meta['Variable Code'] = variable
            series_meta = self.get_meta(variable)
            series_data = operators.rebase(self.get_data(df, variable_u1) / self.get_data(df, variable_o1), BASE_PERIOD)
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        # GNI (GDP deflator)
        variable = 'OVGN.1.0.0.0'
        variable_6 = 'OVGN.6.0.0.0'
        gross_income = 'UVGN.1.0.0.0'
        gross_domestic_product = 'PVGD.3.1.0.0'
        series_meta = self.get_meta(variable)
        series_data = self.get_data(df, gross_income) / self.get_data(self.result, gross_domestic_product) * 100
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        series_meta = self.get_meta(variable_6)
        series_data = series_data.copy().pct_change() * 100
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, 'output/outputvars7.txt', 'output/output7.xlsx')
        return self.result
