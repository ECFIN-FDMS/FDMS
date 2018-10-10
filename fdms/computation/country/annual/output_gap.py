import pandas as pd

from fdms.utils.mixins import StepMixin
from fdms.utils.series import get_series, get_series_noindex, export_to_excel


# STEP 9
class OutputGap(StepMixin):
    def perform_computation(self, output_gap_df):
        variables = ['ZNAWRU.1.0.0.0', 'AVGDGP.1.0.0.0', 'AVGDGT.1.0.0.0', 'OVGDP.1.0.0.0', 'OVGDT.1.0.0.0']
        for variable in variables:
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = get_series(output_gap_df, self.country, variable)
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'OVGDP.6.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'billions'}
        series_data = get_series_noindex(self.result, self.country, 'OVGDP.1.0.0.0').pct_change()
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_to_excel(self.result, 'output/outputvars9.txt', 'output/output9.xlsx')
        return self.result
