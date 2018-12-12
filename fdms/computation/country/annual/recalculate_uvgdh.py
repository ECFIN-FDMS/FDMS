import pandas as pd
import re

from fdms.config.variable_groups import NA_IS_VA
from fdms.utils.mixins import StepMixin
from fdms.utils.series import export_to_excel
from fdms.utils.splicer import Splicer


# STEP 6
class RecalculateUvgdh(StepMixin):
    def perform_computation(self, df, ameco_df):
        uvgdh, uvgdh_1, knp = 'UVGDH', 'UVGDH.1.0.0.0', 'KNP.1.0.212.0'
        series_meta = self.get_meta(uvgdh)
        splicer = Splicer()
        try:
            series_data = self.get_data(ameco_df, uvgdh_1)
            series_data = splicer.ratio_splice(series_data, self.get_data(df, uvgdh_1), type='forward')
        except KeyError:
            series_data = self.get_data(df, uvgdh)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        series_meta = self.get_meta(knp)
        series_data = self.get_data(ameco_df, knp)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, step=6, country=self.country)

        return self.result
