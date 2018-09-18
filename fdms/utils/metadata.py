import pandas as pd


FILENAME_VARS = 'fdms/sample_data/vargroups.xlsx'
SHEET_NAME_VARS = 'vargroups'
FILENAME_COUNTRIES = 'fdms/sample_data/countrygroups.xlsx'
SHEET_NAME_COUNTRIES = 'countrygroups'


def get_vargroups_from_xls(filename=FILENAME_VARS, sheet_name=SHEET_NAME_VARS):
    df = pd.read_excel(filename, sheet_name=sheet_name)
    group_list = df['Group - Code'].unique().tolist()
    groups = {}
    for group in group_list:
        groups[group] = df.loc[df['Group - Code'] == group]['Element - AMECO'].tolist()
    return groups


def get_countrygroups_from_xls(filename=FILENAME_COUNTRIES, sheet_name=SHEET_NAME_COUNTRIES):
    df = pd.read_excel(filename, sheet_name=sheet_name)
    group_list = df['Group - ISO'].unique().tolist()
    groups = {}
    for group in group_list:
        groups[group] = df.loc[df['Group - ISO'] == group]['Element - AMECO'].tolist()
    return groups
