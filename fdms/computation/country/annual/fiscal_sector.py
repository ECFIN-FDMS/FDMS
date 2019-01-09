import pandas as pd

from fdms.config.country_groups import EU
from fdms.utils.mixins import SumAndSpliceMixin
from fdms.utils.splicer import Splicer
from fdms.utils.series import export_to_excel


# STEP 12
class FiscalSector(SumAndSpliceMixin):
    def perform_computation(self, df, ameco_h_df):
        splicer = Splicer()
        addends = {
            'UTOG.1.0.0.0': ['UROG.1.0.0.0', 'UPOMN.1.0.0.0'],
            'UUCG.1.0.0.0': ['UWCG.1.0.0.0', 'UYTGH.1.0.0.0', 'UYIG.1.0.0.0', 'UYVG.1.0.0.0', 'UUOG.1.0.0.0',
                             'UCTGI.1.0.0.0', 'UYTGM.1.0.0.0'],
            'URCG.1.0.0.0': ['UTVG.1.0.0.0', 'UTYG.1.0.0.0', 'UTSG.1.0.0.0', 'UTOG.1.0.0.0'],
            'UUTG.1.0.0.0': ['UUCG.1.0.0.0', 'UIGG0.1.0.0.0', 'UKOG.1.0.0.0'],
            'URTG.1.0.0.0': ['URCG.1.0.0.0', 'UKTTG.1.0.0.0'],
            'UBLG.1.0.0.0': ['URTG.1.0.0.0', '-UUTG.1.0.0.0'],
        }
        # if country == JP: addends['UUCG.1.0.0.0'][0] = 'UCTG.1.0.0.0'; del(addends['UTOG.1.0.0.0'])

        if self.country == 'JP':
            addends['UUCG.1.0.0.0'][0] = 'UCTG.1.0.0.0'
            del addends['UTOG.1.0.0.0']

        self._sum_and_splice(addends, df, ameco_h_df)

        # variable = 'UBLG.1.0.0.0'
        # sources = {variable: ['URTG.1.0.0.0', 'UUTG.1.0.0.0']}
        # series_meta = self.get_meta(variable)
        # splice_series = self.get_data(df, sources[variable][0]).subtract(self.get_data(
        #     df, sources[variable][1], fill_value=0))
        # if self.country == 'JP':
        #     series_data = splice_series.copy()
        # else:
        #     base_series = self.get_data(ameco_h_df, variable)
        #     series_data = splicer.butt_splice(base_series, splice_series, kind='forward')
        # series = pd.Series(series_meta)
        # series = series.append(series_data)
        # self.result = self.result.append(series, ignore_index=True, sort=True)

        if self.country not in EU:
            if self.country != 'MK':
                variable = 'UBLGE.1.0.0.0'
                series_meta = self.get_meta(variable)
                series_data = self.get_data(self.result, 'UBLG.1.0.0.0')
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

                variable = 'UYIGE.1.0.0.0'
                series_meta = self.get_meta(variable)
                series_data = self.get_data(df, 'UYIG.1.0.0.0')
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

        addends = {
            'UBLGI.1.0.0.0': ['UBLG.1.0.0.0', 'UYIG.1.0.0.0'],
            'UBLGIE.1.0.0.0': ['UBLGE.1.0.0.0', 'UYIGE.1.0.0.0'],
            'UTAT.1.0.0.0': ['UTVG.1.0.0.0', 'UTYG.1.0.0.0', 'UTAG.1.0.0.0', 'UTKG.1.0.0.0', 'UTEU.1.0.0.0'],
            'UOOMS.1.0.0.0': ['UOOMSR.1.0.0.0', 'UOOMSE.1.0.0.0'],
            'UTTG.1.0.0.0': ['UTVG.1.0.0.0', 'UTEU.1.0.0.0'],
            'UDGGL.1.0.0.0': ['UDGG.1.0.0.0', ]
        }
        self._sum_and_splice(addends, df, ameco_h_df)

        variable = 'UDGG.1.0.0.0'
        series_meta = self.get_meta(variable)
        series_data = self.get_data(self.result, 'UDGGL.1.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        # TODO: copy EATTG, EATYG and EATSG from cyclical adjustment database
        # for variable in ['EATTG', 'EATYG', 'EATSG']:
        #     series_meta = self.get_meta(variable)
        #     series_data = self.get_data(self.result, 'UDGGL.1.0.0.0')
        #     series = pd.Series(series_meta)
        #     series = series.append(series_data)
        #     self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, step=12, country=self.country)
        return self.result
