import pandas as pd
import re

from fdms.computation.country.annual.transfer_matrix import TransferMatrix


FORECAST = 'fdms/sample_data/BE.Forecast.0908.xlsm'
AMECO = 'fdms/sample_data/BE_AMECO.xlsx'
SHEET = 'BE'


class Compute:
    def __init__(self, country_forecast_filename=FORECAST, ameco_filename=AMECO, ameco_sheet_name=SHEET):
        self.excel_raw = country_forecast_filename
        self.ameco_filename = ameco_filename
        self.ameco_sheet_name = ameco_sheet_name

    def perform_computation(self):
        df, ameco_df = self.read_raw_data(self.excel_raw, self.ameco_filename, self.ameco_sheet_name)
        step_1 = TransferMatrix()
        result_1 = step_1.perform_computation(df, ameco_df)

    def read_raw_data(self, country_forecast_filename, ameco_filename, ameco_sheet_name, frequency='annual'):
        sheet_name = 'Transfer FDMS+ Q' if frequency == 'quarterly' else 'Transfer FDMS+ A'
        df = pd.read_excel(country_forecast_filename, sheet_name=sheet_name, header=10, index_col=[1, 3])
        ameco_df = pd.read_excel(ameco_filename, sheet_name=ameco_sheet_name, index_col=[0, 1])
        ameco_df.rename(columns={c: int(c) for c in ameco_df.columns if re.match('^\d+$', c)}, inplace=True)
        return df, ameco_df