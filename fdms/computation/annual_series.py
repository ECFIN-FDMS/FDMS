import pandas as pd

from fdms.computation.country.annual.transfer_matrix import TransferMatrix

class Compute:
    def __init__(self, country_forecast_filename):
        self.excel_raw = country_forecast_filename

    def perform_computation(self):
        df = self.read_raw_data(self.excel_raw)
        step_1 = TransferMatrix()
        result_1 = step_1.perform_computation()

    def read_raw_data(self, country_forecast_filename):
        return pd.read_excel(country_forecast_filename, sheet_name='Transfer FDMS+ A', header=10, index_col=[1, 3])
