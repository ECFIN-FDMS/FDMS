import pandas as pd

from fdms.config import VARS_FILENAME, EXCEL_FILENAME, COLUMN_ORDER
from fdms.config.scale_correction import SCALES


def get_series(dataframe, country_ameco, variable_code, metadata=False, null_dates=None):
    '''Get quarterly or yearly data from dataframe with indexes "Country AMECO" and "Variable Code"'''
    dataframe.sort_index(level=[0, 1], inplace=True)
    if metadata is True:
        series = dataframe.loc[(country_ameco, variable_code)]
        frequency = series.get('Frequency') if series.get('Frequency') is not None else 'Annual'
        frequency = frequency if type(frequency) == str else frequency.name
        scale = series.get('Scale') if series.get('Scale') is not None else series.get('Unit of the series')
        expected_scale = SCALES.get(variable_code)
        if expected_scale is not None:
            scale = expected_scale
        scale = scale if type(scale) == str else scale.name
        series_meta = {'Country Ameco': country_ameco, 'Variable Code': variable_code, 'Frequency': frequency,
                       'Scale': scale}
        return series_meta
    series = dataframe.loc[(country_ameco, variable_code)].filter(regex='\d{4}')
    if series.empty:
        series = dataframe.loc[(country_ameco, variable_code)].filter(regex='\d{4}Q[1234]')
    if series.empty:
        return None
    # TODO: Log these and make sure that this is correct, check values and get the best one
    if len(series.shape) > 1:
        series = series.iloc[0]
    series = pd.to_numeric(series.squeeze(), errors='coerce')
    if null_dates is not None:
        for year in null_dates:
            series[year] = pd.np.nan
    return series


# def self.get_data(dataframe, country_ameco, variable_code, metadata=False, null_dates=None):
#     '''Get quarterly or yearly data from dataframe with default RangeIndex from "Country AMECO" and "Variable Code"'''
#     result_series_index = dataframe.loc[(dataframe['Country Ameco'] == country_ameco) & (
#             dataframe['Variable Code'] == variable_code)].index.values[0]
#     series = dataframe.loc[result_series_index]
#     series_meta = {'Country Ameco': series['Country Ameco'], 'Variable Code': series['Variable Code'],
#                    'Frequency': series['Frequency'], 'Scale': SCALES.get(variable_code) or series['Scale']}
#     if metadata is True:
#         return series_meta
#     series = series.filter(regex='\d{4}')
#     if series.empty:
#         series = dataframe.loc[result_series_index].filter(regex='\d{4}Q[1234]')
#     if series.empty:
#         return None
#     if len(series.shape) > 1:
#         series = series.iloc[0]
#     series = pd.to_numeric(series.squeeze(), errors='coerce')
#     if null_dates is not None:
#         for year in null_dates:
#             series[year] = pd.np.nan
#     return series


def get_index(dataframe, country_ameco, variable_code):
    return dataframe.loc[(dataframe['Country Ameco'] == country_ameco) & (
            dataframe['Variable Code'] == variable_code)].index.values[0]


# TODO: also fix (two times this returns two series)
def get_scale(dataframe, country_ameco, variable_code):
    dataframe.sort_index(level=[0, 1], inplace=True)
    scale = dataframe.loc[(country_ameco, variable_code)]['Scale']
    if type(scale) == str:
        return scale
    return scale.squeeze()


def get_frequency(dataframe, country_ameco, variable_code):
    dataframe.sort_index(level=[0, 1], inplace=True)
    frequency = dataframe.loc[(country_ameco, variable_code)]['Frequency']
    if type(frequency) == str:
        return frequency
    return frequency.squeeze()


def export_to_excel(result, vars_filename=VARS_FILENAME, excel_filename=EXCEL_FILENAME, sheet_name='Sheet1'):
    column_order = COLUMN_ORDER
    export_data = result.copy()
    export_data = export_data.reset_index()
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                       sheet_name=sheet_name, index=False)
    result_vars = result.index.get_level_values('Variable Code').tolist()
    with open(vars_filename, 'w') as f:
        f.write('\n'.join(result_vars))


def report_diff(result, expected, diff=None, diff_series=None, excel_filename='output/outputdiff.xlsx'):
    column_order = COLUMN_ORDER
    # TODO: Fix all scales
    # column_order.remove('Scale')
    diff = (expected == result) | (expected != expected) & (result != result)
    result = result.reset_index()
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    result[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')], sheet_name='result',
                                  index=False)
    expected = expected.reset_index()
    expected[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')], sheet_name='expected',
                                    index=False)
    diff_series = diff.all(axis=1)
    diff = diff.reset_index()
    diff[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')], sheet_name='diff',
                                index=False)
    # if diff_series:
    #     diff_series = diff_series.reset_index()
    #     diff_series.to_excel(writer, sheet_name='diff_series', index=False)
    writer.save()


def remove_duplicates(result):
    result = result.reset_index()
    result.drop_duplicates(['Country Ameco', 'Variable Code'], keep='last', inplace=True)
    result = result.set_index(['Country Ameco', 'Variable Code'])
    return result


def apply_scale(series_meta, series_data):
    if series_meta['Scale'] == 'billions':
        series_data = series_data * 1E9
    elif series_meta['Scale'] == 'millions':
        series_data = series_data * 1E6
    elif series_meta['Scale'] == 'thousands':
        series_data = series_data * 1000
    return series_meta, series_data
