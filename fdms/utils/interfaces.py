'''
Naming conventions:
    In order to make it easier to read the data from the different files we will name them as follows:

    - Country Forecast excel file: `'{}.forecast.{}.xlsm'.format(country, year)`
    - Country expected result: `'{}.exp.xls'.format(country)`
    - AMECO Historical data: `AMECO_H.TXT`
    - AMECO current excel file for country: `'{}_AMECO.xlsx'.format(country)`
    - Output Gap database: `OUTPUT_GAP.xlsx`
    - Exchange rates database: `XR_IR.xlsx`
    - Cycolical Adjustment: `CYCLICAL_ADJUSTMENT.xlsx`
'''
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(filename='error.log',
                    format='{%(pathname)s:%(lineno)d} - %(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)


import pandas as pd
import re

from fdms.config import AMECO, FORECAST, COLUMN_ORDER
from fdms.config.countries import COUNTRIES
from fdms.config.country_groups import ALL_COUNTRIES


def _get_iso(ameco_code):
    return COUNTRIES['ameco_code']


def _get_ameco(iso_code):
    return COUNTRIES[COUNTRIES == iso_code].index[0]


def _get_from_series_code(series_code, param='variable'):
    parts = series_code.split('.')
    if param == 'country':
        return parts[0]
    return '.'.join([parts[-1], *parts[1:-1]])


def read_country_forecast_excel(country_forecast_filename=FORECAST, frequency='annual', country=None):
    if country in ALL_COUNTRIES:
        country_forecast_filename = '{}.Forecast.xlsm'.format(country)
    sheet_name = 'Transfer FDMS+ Q' if frequency == 'quarterly' else 'Transfer FDMS+ A'
    df = pd.read_excel(country_forecast_filename, sheet_name=sheet_name, header=10, index_col=[1, 3])
    df = df.reset_index()
    df.rename(columns={'Variable': 'Variable Code', 'Country': 'Country Ameco'}, inplace=True)
    df = df.set_index(['Country Ameco', 'Variable Code'])
    return df


def read_ameco_txt(ameco_filename=AMECO):
    with open(ameco_filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    ameco_df = pd.DataFrame.from_records([line.split(',') for line in lines[1:]], columns=lines[0].split(','))
    ameco_df = ameco_df.set_index('CODE')
    ameco_df['Country Ameco'] = ameco_df.apply(lambda row: _get_ameco(_get_from_series_code(row.name, 'country')),
                                               axis=1)
    ameco_df['Variable Code'] = ameco_df.apply(lambda row: _get_from_series_code(row.name, 'variable'), axis=1)
    ameco_df.rename(columns={c: int(c) for c in ameco_df.columns if re.match('^[0-9]+$', c)}, inplace=True)
    ameco_df = ameco_df.reset_index()
    ameco_df = ameco_df.set_index(['Country Ameco', 'Variable Code'])
    return ameco_df


def read_expected_result(xls_export='fdms/sample_data/BE.exp.xlsx', country=None):
    if country in ALL_COUNTRIES:
        xls_export = 'fdms/sample_data/{}.exp.xlsx'.format(country)
    df = pd.read_excel(xls_export, sheet_name='Sheet1')
    df.rename(columns={c: int(c) for c in df.columns if re.match('^[0-9]+$', str(c))}, inplace=True)
    df.rename(columns={'Variable': 'Variable Code', 'Country': 'Country Ameco'}, inplace=True)
    df = df.reset_index()
    df = df.set_index(['Country Ameco', 'Variable Code'])
    return df


def read_expected_result_be(xls_export='fdms/sample_data/BE_expected_scale.xlsx'):
    df = pd.read_excel(xls_export, sheet_name='BE', index_col=[0, 1])
    df = df.reset_index()
    df.rename(columns={c: int(c) for c in df.columns if re.match('^[0-9]+$', c)}, inplace=True)
    df.rename(columns={'Scale Name': 'Scale', 'Country AMECO': 'Country Ameco'}, inplace=True)
    df['Frequency'] = 'Annual'
    df = df.set_index(['Country Ameco', 'Variable Code'])
    return df


def read_raw_data(country_forecast_filename, ameco_filename, ameco_sheet_name, frequency='annual'):
    sheet_name = 'Transfer FDMS+ Q' if frequency == 'quarterly' else 'Transfer FDMS+ A'
    df = pd.read_excel(country_forecast_filename, sheet_name=sheet_name, header=10, index_col=[1, 3])
    ameco_df = pd.read_excel(ameco_filename, sheet_name=ameco_sheet_name, index_col=[0, 1])
    ameco_df.rename(columns={c: int(c) for c in ameco_df.columns if re.match('^[0-9]+$', c)}, inplace=True)
    return df, ameco_df


# TODO: check if we're using ameco historic instead of this one in some places by mistake
def read_ameco_db_xls(ameco_db_excel='fdms/sample_data/BE_AMECO.xlsx', frequency='annual', all_data=False):
    sheet_name = 'BE'
    df = pd.read_excel(ameco_db_excel, sheet_name=sheet_name, index_col=[0, 1])
    df = df.reset_index()
    df.rename(columns={c: int(c) for c in df.columns if re.match('^[0-9]+$', c)}, inplace=True)
    df.rename(columns={'Scale Name': 'Scale', 'Country AMECO': 'Country Ameco'}, inplace=True)
    df['Frequency'] = 'Annual'
    # TODO: We need to update this db?
    if 2019 not in df.columns:
        df[2019] = pd.np.nan
    if all_data is False:
        df = df[COLUMN_ORDER]
    df = df.set_index(['Country Ameco', 'Variable Code'])
    return df


def read_output_gap_xls(output_gap_excel='fdms/sample_data/OUTPUT_GAP.xlsx', frequency='annual'):
    sheet_name = 'output_gap'
    df = pd.read_excel(output_gap_excel, sheet_name=sheet_name, index_col=[0, 1])
    df = df.reset_index()
    df.rename(columns={c: int(c) for c in df.columns if re.match('^[0-9]+$', c)}, inplace=True)
    df.rename(columns={'Scale Name': 'Scale', 'Country AMECO': 'Country Ameco'}, inplace=True)
    df['Frequency'] = 'Annual'
    df = df.set_index(['Country Ameco', 'Variable Code'])
    return df


def read_xr_ir_xls(output_gap_excel='fdms/sample_data/XR_IR.xlsx', frequency='annual'):
    sheet_name = 'xr-ir'
    df = pd.read_excel(output_gap_excel, sheet_name=sheet_name, index_col=[0, 1])
    df = df.reset_index()
    df.rename(columns={c: int(c) for c in df.columns if re.match('^[0-9]+$', c)}, inplace=True)
    df.rename(columns={'Scale Name': 'Scale', 'Country AMECO': 'Country Ameco'}, inplace=True)
    df['Frequency'] = 'Annual'
    df = df.set_index(['Country Ameco', 'Variable Code'])
    return df


def read_ameco_xne_us_xls(ameco_xne_us_excel='fdms/sample_data/AMECO_XNE_US.xlsx', frequency='annual'):
    sheet_name = 'ameco_xne_us'
    df = pd.read_excel(ameco_xne_us_excel, sheet_name=sheet_name, index_col=[0, 1])
    df = df.reset_index()
    df.rename(columns={c: int(c) for c in df.columns if re.match('^[0-9]+$', c)}, inplace=True)
    df.rename(columns={'Scale Name': 'Scale', 'Country AMECO': 'Country Ameco'}, inplace=True)
    df['Frequency'] = 'Annual'
    df = df.set_index(['Country Ameco', 'Variable Code'])
    return df


def get_fc(country='BE', frequency='annual'):
    sheet_name = 'Transfer FDMS+ Q' if frequency == 'quarterly' else 'Transfer FDMS+ A'
    country_forecast_filename = 'fdms/sample_data/{}.Forecast.SF2018.xlsm'.format(country)
    df = pd.read_excel(country_forecast_filename, sheet_name=sheet_name, header=10, index_col=[1, 3])
    return df


def get_scales_from_forecast(country='BE', frequency='annual'):
    df = get_fc(country, frequency)
    scales = {index[1] + '.1.0.0.0': df.loc[index, 'Scale'].capitalize() for index in df.index}
    scales.update({index[1]: df.loc[index, 'Scale'].capitalize() for index in df.index})
    return scales
