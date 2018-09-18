import logging


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s', level=logging.INFO)


import pandas as pd
import re

from fdms.config.countries import COUNTRIES


AMECO = 'fdms/sample_data/AMECO_H.TXT'
FORECAST = 'fdms/sample_data/LT.Forecast.SF2018.xlsm'


def read_country_forecast_excel(country_forecast_filename=FORECAST, frequency='annual'):
    sheet_name = 'Transfer FDMS+ Q' if frequency == 'quarterly' else 'Transfer FDMS+ A'
    df = pd.read_excel(country_forecast_filename, sheet_name=sheet_name, header=10, index_col=[1, 3])
    return df


def read_ameco_txt(ameco_filename=AMECO):
    with open(ameco_filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    ameco_df = pd.DataFrame.from_records([line.split(',') for line in lines[1:]], columns=lines[0].split(','))
    ameco_df = ameco_df.set_index('CODE')
    ameco_df['Country Ameco'] = ameco_df.apply(lambda row: _get_ameco(_get_from_series_code(row.name, 'country')), axis=1)
    ameco_df['Variable Code'] = ameco_df.apply(lambda row: _get_from_series_code(row.name, 'variable'), axis=1)
    ameco_df.rename(columns={c: int(c) for c in ameco_df.columns if re.match('^\d+$', c)}, inplace=True)
    ameco_df = ameco_df.reset_index()
    ameco_df = ameco_df.set_index(['Country Ameco', 'Variable Code'])
    return ameco_df


def read_expected_result(xls_export='fdms/sample_data/BE.exp.xlsx'):
    df = pd.read_excel(xls_export, sheet_name='Table')
    df.rename(columns={c: int(c) for c in df.columns if re.match('^\d+$', c)}, inplace=True)
    df = df.reset_index()
    df = df.set_index(['Country', 'Variable'])
    return df


def read_raw_data(country_forecast_filename, ameco_filename, ameco_sheet_name, frequency='annual'):
    sheet_name = 'Transfer FDMS+ Q' if frequency == 'quarterly' else 'Transfer FDMS+ A'
    df = pd.read_excel(country_forecast_filename, sheet_name=sheet_name, header=10, index_col=[1, 3])
    ameco_df = pd.read_excel(ameco_filename, sheet_name=ameco_sheet_name, index_col=[0, 1])
    ameco_df.rename(columns={c: int(c) for c in ameco_df.columns if re.match('^\d+$', c)}, inplace=True)
    return df, ameco_df