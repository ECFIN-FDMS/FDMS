import pandas as pd

from fdms.utils.mixins import SumAndSpliceMixin
from fdms.utils.splicer import Splicer
from fdms.utils.operators import Operators
from fdms.utils.series import export_to_excel


# STEP 16
class ExternalSector(SumAndSpliceMixin):
    def perform_computation(self, result_1, result_3, ameco_h_df):
        # TODO: Check the scales of the output variables
        splicer = Splicer()
        operators = Operators()

        # UBYA.1.0.0.0

        addends = {'UBYA.1.0.0.0': ['UBRA.1.0.0.0', 'UBTA.1.0.0.0']}
        self._sum_and_splice(addends, result_1, ameco_h_df, splice=False)
        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1, result_3], sort=True)


        # UBCA.1.0.0.0

        addends = {'UBCA.1.0.0.0': ['UXGS.1.0.0.0', '-UMGS.1.0.0.0', 'UBYA.1.0.0.0']}
        self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)
        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1, result_3], sort=True)

        # UBLA.1.0.0.0

        addends = {'UBLA.1.0.0.0': ['UBCA.1.0.0.0', 'UBKA.1.0.0.0']}
        self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

        # DXGT.1.0.0.0

        dxge_data = self.get_data(new_input_df, 'DXGE.1.0.0.0')
        dxgi_data = self.get_data(new_input_df, 'DXGI.1.0.0.0')
        dxgt_data = dxge_data + dxgi_data
        series_meta = self.get_meta('DXGT.1.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(dxgt_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1], sort=True)

        # DMGT.1.0.0.0

        dmge_data = self.get_data(new_input_df, 'DMGE.1.0.0.0')
        dmgi_data = self.get_data(new_input_df, 'DMGI.1.0.0.0')
        dmgt_data = dmge_data + dmgi_data
        series_meta = self.get_meta('DMGT.1.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(dmgt_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1], sort=True)

        # DBGT.1.0.0.0

        dxgt_data = self.get_data(new_input_df, 'DXGT.1.0.0.0')
        dmgt_data = self.get_data(new_input_df, 'DMGT.1.0.0.0')
        dbgt_data = dxgt_data - dmgt_data
        series_meta = self.get_meta('DBGT.1.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(dbgt_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        # DBGE.1.0.0.0

        dxge_data = self.get_data(new_input_df, 'DXGT.1.0.0.0')
        dmge_data = self.get_data(new_input_df, 'DMGT.1.0.0.0')
        dbge_data = dxge_data - dmge_data
        series_meta = self.get_meta('DBGE.1.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(dbge_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        # TODO: DBGI.1.0.0.0

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()

        export_to_excel(self.result, step=16)


        return self.result