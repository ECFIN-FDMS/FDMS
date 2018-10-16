import pandas as pd
import re

from fdms.config.country_groups import EU
from fdms.utils.mixins import StepMixin, SumAndSpliceMixin
from fdms.utils.splicer import Splicer
from fdms.utils.operators import Operators
from fdms.utils.series import get_series, get_series_noindex, export_to_excel


# STEP 13
class CorporateSector(StepMixin, SumAndSpliceMixin):
    def perform_computation(self, df, ameco_h_df):
        splicer = Splicer()
        operators = Operators()
        addends = {
            'USGC.1.0.0.0': ['UGVAC.1.0.0.0', 'UYVC.1.0.0.0', '-UTVC.1.0.0.0', '-UWCC.1.0.0.0', 'UYNC.1.0.0.0',
                             'UCTRC.1.0.0.0', '-UTYC.1.0.0.0', '-UEHC.1.0.0.0'],
            'UBLC.1.0.0.0': ['USGC.1.0.0.0', '-UITC.1.0.0.0', '-UKOC.1.0.0.0'],
        }

        if self.country == 'JP':
            del addends['USGC.1.0.0.0']

        self._sum_and_splice(addends, df, ameco_h_df)

        variable = 'UOGC.1.0.0.0'
        sources = {variable: ['URTG.1.0.0.0', 'UUTG.1.0.0.0']}
        series_meta = self.get_meta(variable)
        base_series = get_series(ameco_h_df, self.country, variable)
        new_data = get_series(df, self.country, 'UGVAC.1.0.0.0') + get_series(
            df, self.country, 'UYVC.1.0.0.0') - get_series(df, self.country, 'UTVC.1.0.0.0') - get_series(
            df, self.country, 'UWCC.1.0.0.0')
        value_if_null = get_series(df, self.country, 'UOGC.1.0.0.0'), get_series(
            df, self.country, 'UGVAC.1.0.0.0') + get_series(df, self.country, 'UYVC.1.0.0.0') - get_series(
            df, self.country, 'UTVC.1.0.0.0') - get_series(df, self.country, 'UWCC.1.0.0.0')
        series_data = splicer.butt_splice(base_series, operators.iin(new_data, value_if_null))

        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, 'output/outputvars13.txt', 'output/output13.xlsx')
        return self.result
