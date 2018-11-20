import pandas as pd

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
        # import pdb;pdb.set_trace()
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

        import code;code.interact(local=locals())

        # addends = {
        #     'USGC.1.0.0.0': ['UGVAC.1.0.0.0', 'UYVC.1.0.0.0', '-UTVC.1.0.0.0', '-UWCC.1.0.0.0', 'UYNC.1.0.0.0',
        #                      'UCTRC.1.0.0.0', '-UTYC.1.0.0.0', '-UEHC.1.0.0.0'],
        #     'UBLC.1.0.0.0': ['USGC.1.0.0.0', '-UITC.1.0.0.0', '-UKOC.1.0.0.0'],
        # }

        # self._sum_and_splice(addends, df, ameco_h_df)

        # variable = 'UOGC.1.0.0.0'
        # sources = {variable: ['URTG.1.0.0.0', 'UUTG.1.0.0.0']}
        # series_meta = self.get_meta(variable)
        # base_series = self.get_data(ameco_h_df, variable)
        # new_data = self.get_data(df, 'UGVAC.1.0.0.0') + self.get_data(df, 'UYVC.1.0.0.0') - self.get_data(
        #     df, 'UTVC.1.0.0.0') - self.get_data(df, 'UWCC.1.0.0.0')
        # value_if_null = self.get_data(df, 'UOGC.1.0.0.0')
        # value = self.get_data(df, 'UGVAC.1.0.0.0') + self.get_data(df, 'UYVC.1.0.0.0') - self.get_data(
        #     df, 'UTVC.1.0.0.0') - self.get_data(df, 'UWCC.1.0.0.0')
        # series_data = splicer.butt_splice(base_series, operators.iin(new_data, value_if_null, value))

        # series = pd.Series(series_meta)
        # series = series.append(series_data)
        # self.result = self.result.append(series, ignore_index=True, sort=True)

        # self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        # self.apply_scale()
        # export_to_excel(self.result, 'output/outputvars13.txt', 'output/output13.xlsx')
        # return self.result
