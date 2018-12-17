import pandas as pd

from fdms.utils.mixins import SumAndSpliceMixin
from fdms.utils.splicer import Splicer
from fdms.utils.operators import Operators
from fdms.utils.series import export_to_excel


# STEP 15
class PrivateSector(SumAndSpliceMixin):
    def perform_computation(self, result_1, result_12, result_13, result_14, ameco_h_df):
        breakpoint()
        # TODO: Check the scales of the output variables
        splicer = Splicer()
        operators = Operators()

        # USGN.1.0.0.0

        addends = {'USGN.1.0.0.0': ['UVGD', 'UBRA', 'UBTA', '-UCPH', '-UCTG']}

        self._sum_and_splice(addends, result_1, ameco_h_df, splice=False)
        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1, result_13, result_14], sort=True)

        # UBLP.1.0.0.0

        addends = {'UBLP.1.0.0.0': ['UBLC.1.0.0.0', 'UBLH.1.0.0.0']}

        self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)
        new_input_df = self.result.set_index(['Country Ameco', 'Variable Code'], drop=True)
        new_input_df = pd.concat([new_input_df, result_1, result_12], sort=True)

        # USGP.1.0.0.0

        addends = {'USGP.1.0.0.0': ['USGN.1.0.0.0','USGG.1.0.0.0']}

        self._sum_and_splice(addends, new_input_df, ameco_h_df, splice=False)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()

        export_to_excel(self.result, step=15)

        return self.result