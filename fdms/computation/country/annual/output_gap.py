import pandas as pd

from fdms.utils.mixins import StepMixin
from fdms.utils.series import export_to_excel


# STEP 9
class OutputGap(StepMixin):
    def perform_computation(self, output_gap_df):
        variables = ['ZNAWRU.1.0.0.0', 'AVGDGP.1.0.0.0', 'AVGDGT.1.0.0.0', 'OVGDP.1.0.0.0', 'OVGDT.1.0.0.0']
        for variable in variables:
            series_meta = self.get_meta(variable)
            series_data = self.get_data(output_gap_df, variable)
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'OVGDP.6.0.0.0'
        series_meta = self.get_meta(variable)
        series_data = self.get_data(self.result, 'OVGDP.1.0.0.0').pct_change() * 100
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, step=9, country=self.country)
        return self.result
