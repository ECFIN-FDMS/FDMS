import pandas as pd

from fdms.config import BASE_PERIOD
from fdms.utils.mixins import SumAndSpliceMixin
from fdms.utils.splicer import Splicer
from fdms.utils.operators import Operators
from fdms.utils.series import export_to_excel


# STEP 14
class HouseholdSector(SumAndSpliceMixin):
    def perform_computation(self, result_1, result_7, ameco_h_df):
        splicer = Splicer()
        operators = Operators()
        # First we will calculate ASGH.1.0.0.0 and OVGHA.3.0.0.0, and then we will use the _sum_and_splice method
        # From SumAndSpliceMixin to calculate all the rest
        addends = {'UYOH.1.0.0.0': ['UOGH.1.0.0.0', 'UYNH.1.0.0.0']}
        self._sum_and_splice(addends, result_1, ameco_h_df, splice=False)
        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1], sort=True)
        addends = {'UVGH.1.0.0.0': ['UWCH.1.0.0.0', 'UYOH.1.0.0.0', 'UCTRH.1.0.0.0', '-UTYH.1.0.0.0', '-UCTPH.1.0.0.0']}
        self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1], sort=True)
        addends = {'UVGHA.1.0.0.0': ['UVGH.1.0.0.0', 'UEHH.1.0.0.0']}
        self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

        addends = {'USGH.1.0.0.0': ['UWCH.1.0.0.0', 'UOGH.1.0.0.0', 'UYNH.1.0.0.0', 'UCTRH.1.0.0.0', '-UTYH.1.0.0.0',
                                    '-UCTPH.1.0.0.0', 'UEHH.1.0.0.0', '-UCPH0.1.0.0.0']}
        self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1], sort=True)
        # Since this formula is using *ignoremissingsubtract* instead of *ignoremissingsum*, we change the sign of all
        # but the first variables in the list
        addends = {'UBLH.1.0.0.0': ['USGH.1.0.0.0', '-UITH.1.0.0.0', '-UKOH.1.0.0.0']}
        self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

        uvgha_data = self.get_data(new_input_df, 'UVGHA.1.0.0.0')
        pcph_data = self.get_data(result_7, 'PCPH.3.1.0.0')
        uvgha_base_period = uvgha_data.loc[BASE_PERIOD]
        ovgha_data = operators.rebase(uvgha_data / pcph_data, BASE_PERIOD) / 100 * uvgha_base_period
        series_meta = self.get_meta('OVGHA.3.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(ovgha_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        usgh_data = self.get_data(new_input_df, 'USGH.1.0.0.0')
        uvgha_data = self.get_data(new_input_df, 'UVGHA.1.0.0.0')
        asgh_ameco_h = self.get_data(ameco_h_df, 'ASGH.1.0.0.0')
        asgh_data = splicer.butt_splice(asgh_ameco_h, usgh_data / uvgha_data * 100)
        series_meta = self.get_meta('ASGH.1.0.0.0')
        new_series = pd.Series(series_meta)
        new_series = new_series.append(asgh_data)
        self.result = self.result.append(new_series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, step=14)
        return self.result
