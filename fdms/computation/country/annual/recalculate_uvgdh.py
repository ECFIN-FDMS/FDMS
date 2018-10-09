import pandas as pd
import re

from fdms.config.variable_groups import NA_IS_VA
from fdms.utils.series import get_series, get_series_noindex, export_to_excel
from fdms.utils.splicer import Splicer


# STEP 6
class RecalculateUvgdh:
    result = pd.DataFrame()
    country = 'BE'
    frequency = 'Annual'

    def perform_computation(self, df, ameco_df):
        uvgdh, uvgdh_1, knp = 'UVGDH', 'UVGDH.1.0.0.0', 'KNP.1.0.212.0'
        series_meta = get_series(df, self.country, uvgdh, metadata=True)
        splicer = Splicer()
        try:
            series_data = get_series(ameco_df, self.country, uvgdh_1)
            series_data = splicer.ratio_splice(series_data, get_series(df, self.country, uvgdh_1), type='forward')
        except KeyError:
            series_data = get_series(df, self.country, uvgdh)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        series_meta = get_series(ameco_df, self.country, knp, metadata=True)
        series_data = get_series(ameco_df, self.country, knp)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_to_excel(self.result, 'output/outputvars6.txt', 'output/output6.xlsx')

        return self.result
