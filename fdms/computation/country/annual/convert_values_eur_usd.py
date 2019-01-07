import pandas as pd

from fdms.utils.mixins import StepMixin
from fdms.utils.splicer import Splicer
from fdms.utils.operators import Operators
from fdms.utils.series import export_to_excel


# STEP 18
class ConvertEurUsd(StepMixin):
    def perform_computation(self, result_1, result_3, ameco_h_df):
        # TODO: All Calculations
        splicer = Splicer()
        operators = Operators()


        # TODO: DBGI.1.0.0.0

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()

        export_to_excel(self.result, step=16)

        return self.result