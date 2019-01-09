import pandas as pd
import os
import re

from fdms.config import VARS_FILENAME, EXCEL_FILENAME, COLUMN_ORDER, PROJECT_ROOT
from fdms.config.country_groups import ALL_COUNTRIES


def get_filenames_for_step(step, country):
    return os.path.join(PROJECT_ROOT, 'output\\{}\\outputvars{}.txt'.format(country, step)), os.path.join(
        PROJECT_ROOT, 'output\\{}\\output{}.xlsx'.format(country, step))


def export_to_excel(result, vars_filename=VARS_FILENAME, excel_filename=EXCEL_FILENAME, step=None, sheet_name='Sheet1',
                    country='BE'):
    if step is not None:
        vars_filename, excel_filename = get_filenames_for_step(step, country)
    column_order = COLUMN_ORDER
    export_data = result.copy()
    export_data = export_data.reset_index()
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                       sheet_name=sheet_name, index=False)
    result_vars = result.index.get_level_values('Variable Code').tolist()
    # We shouldn't need this line
    output_dir = os.path.join(PROJECT_ROOT, 'output\\{}'.format(country))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    assert(os.path.exists(output_dir))
    with open(vars_filename, 'w') as f:
        f.write('\n'.join(result_vars))


def report_diff(result, expected, diff=None, diff_series=None, country=None, excel_filename='output/outputdiff.xlsx'):
    column_order = COLUMN_ORDER
    # TODO: Fix all scales
    # column_order.remove('Scale')
    diff = (expected == result) | (expected != expected) & (result != result)
    result = result.reset_index()
    if country in ALL_COUNTRIES:
        excel_filename = 'output/{}/outputdiff.xlsx'.format(country)
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


def get_input_series(country_excel='fdms/sample_data/IT_DB_orig.xlsx', sheet_name='A1996'):
    df = pd.read_excel(country_excel, sheet_name=sheet_name, index_col=[0, 1])
    result = pd.DataFrame()
    df.rename(columns={'Variable': 'Variable Code', 'Country': 'Country Ameco'}, inplace=True)
    for index, row in df.iterrows():
        if not re.match('.*\.', row['Variable Code']):
            result = result.append(row, ignore_index=True, sort=True)
    result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
    return result