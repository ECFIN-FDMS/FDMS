import pandas as pd
import re

from fdms.config.variable_groups import NA_IS_VA
from fdms.utils.mixins import SumAndSpliceMixin
from fdms.utils.series import export_to_excel


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
        series_data = (self.get_data(df, total_employment) * self.get_data(df, compensation) / self.get_data(
            df, real_compensation))
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        for variable in NA_IS_VA:
            variable_1 = variable + '.1.0.0.0'
            variable_cc = re.sub('^U', 'CC', variable_1)
            series_meta = self.get_meta(variable_cc)
            try:
                pch = self.get_data(self.result, variable_1) / ovgd1
            except (IndexError, KeyError):
                pch = self.get_data(df, variable_1) / ovgd1
            pch = pch.pct_change() * 100
            try:
                series_data = self.get_data(self.result, variable_1) / self.get_data(df, 'UVGD.1.0.0.0') * pch
            except (IndexError, KeyError):
                series_data = self.get_data(df, variable_1) / self.get_data(df, 'UVGD.1.0.0.0') * pch
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, step=5, country=self.country)
        return self.result
