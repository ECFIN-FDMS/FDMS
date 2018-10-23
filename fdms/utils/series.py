import pandas as pd

from fdms.config import VARS_FILENAME, EXCEL_FILENAME, COLUMN_ORDER


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
