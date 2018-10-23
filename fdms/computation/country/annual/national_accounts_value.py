import pandas as pd
import re

from fdms.config.variable_groups import NA_IS_VA
from fdms.utils.mixins import SumAndSpliceMixin
from fdms.utils.series import get_series, export_to_excel


# STEP 5
class NationalAccountsValue(SumAndSpliceMixin):
    def perform_computation(self, df, ameco_db_df, ovgd1):
        addends = {
            'UVGN.1.0.0.0': ['UVGD.1.0.0.0', 'UBRA.1.0.0.0'],
            'UOGD.1.0.0.0': ['UVGD.1.0.0.0', 'UYVG.1.0.0.0', 'UYEU.1.0.0.0', '-UWCD.1.0.0.0', '-UTVG.1.0.0.0',
                             '-UTEU.1.0.0.0'],
            'UTVNBP.1.0.0.0': ['UTVTBP.1.0.0.0', '-UYVTBP.1.0.0.0'],
            'UVGE.1.0.0.0': ['UVGD.1.0.0.0', '-UTVNBP.1.0.0.0'],
            'UWSC.1.0.0.0': ['UWCD.1.0.0.0', '-UWWD'],
        }
        self._sum_and_splice(addends, df, df, splice=False)

        variable = 'UWCDA.1.0.0.0'
        total_employment = 'NETD.1.0.0.0'
        compensation = 'UWCD.1.0.0.0'
        real_compensation = 'NWTD.1.0.0.0'
        series_meta = self.get_meta(variable)
        series_data = (get_series(df, self.country, total_employment) * get_series(df, self.country, compensation) /
                       get_series(df, self.country, real_compensation))
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        for variable in NA_IS_VA:
            variable_1 = variable + '.1.0.0.0'
            variable_cc = re.sub('^U', 'CC', variable_1)
            series_meta = self.get_meta(variable_cc)
            try:
                pch = self.get_data(self.result, variable_1) / ovgd1
            except IndexError:
                pch = get_series(df, self.country, variable_1) / ovgd1
            pch = pch.pct_change() * 100
            try:
                series_data = self.get_data(self.result, variable_1) / get_series(
                    df, self.country, 'UVGD.1.0.0.0') * pch
            except IndexError:
                series_data = get_series(df, self.country, variable_1) / get_series(
                    df, self.country, 'UVGD.1.0.0.0') * pch
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, 'output/outputvars5.txt', 'output/output5.xlsx')
        return self.result
