import pandas as pd

from fdms.utils.mixins import StepMixin
from fdms.utils.series import export_to_excel

# STEP 18
class ConvertEurUsd(StepMixin):

    def perform_computation(self, df):

        processed_vars = []

        for index, row in result.iterrows():
            variable = index
            processed_vars.append(variable)

            # Convert value variables from national currency to euros (99)

            list1 = ['XNE.1.0.99.0', 'XNEF.1.0.99.0', 'XNEB.1.0.99.0']

            if variable not in list1:
                if variable[0] == 'U' and variable[-8:] == '1.0.99.0':
                    xne_data = self.get_data(new_input_df, 'XNE.1.0.99.0')
                    new_variable = variable[:-4] + '0.0'
                    variable = new_variable / xne_data

            # Convert value variables from national currency to USD (30)

            if variable[0] == 'U' and variable[-8:] == '1.0.30.0':
                xnu_data = self.get_data(new_input_df, 'XNU.1.0.30.0')
                new_variable = variable[:-4] + '0.0'
                variable = new_variable / xnu_data

            # Set 6.1.0.0=6.0.0.0 for individual countries

            if variable[-7:] == '6.1.0.0':
                new_variable = variable[:-4] + '6.0.0.0'
                #if new_variable is existing in the dataframe
                variable = new_variable

            # TODO: Set 1.1.0.0=1.0.0.0 for individual countries

            # TODO: Calculate series as a percentage of GDP (310 and 319)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()

        export_to_excel(self.result, step=18)

        return self.result