import datetime

import pandas as pd

from fdms.config import COLUMN_ORDER, LAST_YEAR
from fdms.config.country_groups import EA, get_membership_date
from fdms.utils.mixins import StepMixin
from fdms.utils.series import get_series, get_series_noindex, export_to_excel
from fdms.utils.splicer import Splicer


# STEP 10
class ExchangeRates(StepMixin):
    def perform_computation(self, ameco_db_df, xr_df, ameco_xne_us_df):
        splicer = Splicer()
        variable = 'XNE.1.0.99.0'
        series_data = get_series(ameco_db_df, self.country, variable)
        try:
            xr_data = get_series(xr_df, self.country, variable)
        except KeyError:
            pass
        else:
            last_valid = xr_data.first_valid_index()
            for year in range(last_valid + 1, LAST_YEAR + 1):
                series_data[year] = pd.np.nan
            series_data = splicer.ratio_splice(series_data.copy(), xr_data, kind='forward')
        series_meta = self.get_meta(variable)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        variables = ['ILN.1.0.0.0', 'ISN.1.0.0.0']
        sources = ['ILN.1.1.0.0', 'ISN.1.1.0.0']
        null_dates = list(range(int(datetime.datetime.now().year) - 1, LAST_YEAR))
        for index, variable in enumerate(variables):
            series_meta = self.get_meta(variable)
            series_data = get_series(ameco_db_df, self.country, sources[index], null_dates=null_dates)
            series_data = splicer.butt_splice(series_data, get_series(xr_df, self.country, sources[index]),
                                              kind='forward')
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        if self.country in EA:
            membership_date = get_membership_date(self.country)
            variable = 'XNE.1.0.99.0'
            for year in range(membership_date, LAST_YEAR + 1):
                self.result.loc[self.result['Variable Code'] == 'XNE.1.0.99.0', year] = 1

            variable = 'XNEF.1.0.99.0'
            series_meta = self.get_meta(variable)
            series_data = get_series(ameco_db_df, self.country, 'XNE.1.0.99.0')
            last_valid = series_data.last_valid_index()
            if last_valid < LAST_YEAR:
                for index in range(last_valid + 1, LAST_YEAR + 1):
                    series_data[index] = series_data[last_valid]
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

            variable = 'XNEB.1.0.99.0'
            series_meta = self.get_meta(variable)
            series_data = get_series_noindex(self.result, self.country, 'XNE.1.0.99.0') * get_series_noindex(
                self.result, self.country, 'XNEF.1.0.99.0')
            for year in range(membership_date, LAST_YEAR + 1):
                self.result.loc[self.result['Variable Code'] == 'XNEF.1.0.99.0', year] = pd.np.nan
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
        else:
            variable = 'XNEB.1.0.99.0'
            series_meta = self.get_meta(variable)
            series_data = get_series_noindex(self.result, self.country, 'XNE.1.0.99.0').copy()
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'XNU.1.0.30.0'
        xne_us = get_series(xr_df, 'US', 'XNE.1.0.99.0')
        last_observation = xne_us.first_valid_index()
        new_xne_us = get_series(ameco_xne_us_df, 'US', 'XNE.1.0.99.0')
        for year in range(last_observation + 1, LAST_YEAR + 1):
            new_xne_us[year] = pd.np.nan
        series_meta = self.get_meta(variable)
        series_data = splicer.ratio_splice(new_xne_us, xne_us, kind='forward')
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        # Effective exchange rates and relative unit labour costs, currently not calculated in FDMS+
        variables = ['PLCDQ.3.0.0.437', 'PLCDQ.3.0.30.437', 'XUNNQ.3.0.30.437', 'XUNRQ.3.0.30.437', 'PLCDQ.3.0.0.414',
                     'PLCDQ.3.0.0.415', 'PLCDQ.3.0.0.417', 'PLCDQ.3.0.0.424', 'PLCDQ.3.0.0.427', 'PLCDQ.3.0.0.435',
                     'PLCDQ.3.0.0.436', 'PLCDQ.3.0.30.414', 'PLCDQ.3.0.30.415', 'PLCDQ.3.0.30.417', 'PLCDQ.3.0.30.424',
                     'PLCDQ.3.0.30.427', 'PLCDQ.3.0.30.435', 'PLCDQ.3.0.30.436', 'XUNNQ.3.0.30.414', 'XUNNQ.3.0.30.415',
                     'XUNNQ.3.0.30.417', 'XUNNQ.3.0.30.423', 'XUNNQ.3.0.30.424', 'XUNNQ.3.0.30.427', 'XUNNQ.3.0.30.435',
                     'XUNNQ.3.0.30.436', 'XUNNQ.3.0.30.441', 'XUNRQ.3.0.30.414', 'XUNRQ.3.0.30.415', 'XUNRQ.3.0.30.417',
                     'XUNRQ.3.0.30.424', 'XUNRQ.3.0.30.427', 'XUNRQ.3.0.30.435', 'XUNRQ.3.0.30.436']
        missing_vars = []
        for variable in variables:
            series_meta = self.get_meta(variable)
            try:
                series_data = get_series(ameco_db_df, self.country, variable)
            except KeyError:
                missing_vars.append(variable)
            else:
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

        variables = ['PLCDQ.6.0.0.437', 'PLCDQ.6.0.0.435', 'PLCDQ.6.0.0.436']
        sources = ['PLCDQ.3.0.0.437', 'PLCDQ.3.0.0.435', 'PLCDQ.3.0.0.436']
        for index, variable in enumerate(variables):
            series_meta = self.get_meta(variable)
            try:
                series_data = get_series_noindex(self.result, self.country, sources[index]).copy().pct_change()
            except IndexError:
                missing_vars.append(variable)
            else:
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

        variables = ['XUNNQ.6.0.30.437', 'XUNRQ.6.0.30.437', 'XUNNQ.6.0.30.435', 'XUNNQ.6.0.30.436', 'XUNRQ.6.0.30.435',
                     'XUNRQ.6.0.30.436']
        sources = ['XUNNQ.3.0.30.437', 'XUNRQ.3.0.30.437', 'XUNNQ.3.0.30.435', 'XUNNQ.3.0.30.436', 'XUNRQ.3.0.30.435',
                   'XUNRQ.3.0.30.436']
        for index, variable in enumerate(variables):
            series_meta = self.get_meta(variable)
            try:
                series_data = get_series_noindex(self.result, self.country, sources[index]).copy().pct_change()
            except IndexError:
                missing_vars.append(variable)
            else:
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

        # TODO: is it OK? these are missing in ameco_db: PLCDQ.3.0.0.414 PLCDQ.3.0.0.435 PLCDQ.3.0.0.436
        # PLCDQ.3.0.30.414 PLCDQ.3.0.30.435 PLCDQ.3.0.30.436 XUNNQ.3.0.30.414 XUNNQ.3.0.30.423 XUNNQ.3.0.30.435
        # XUNNQ.3.0.30.436 XUNNQ.3.0.30.441 XUNRQ.3.0.30.414 XUNRQ.3.0.30.435 XUNRQ.3.0.30.436 PLCDQ.6.0.0.435
        # PLCDQ.6.0.0.436
        with open('errors_step_10.txt', 'w') as f:
            f.write('\n'.join(missing_vars))

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, 'output/outputvars10.txt', 'output/output10.xlsx')
        return self.result
