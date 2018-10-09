import pandas as pd

from fdms.config import FILENAME_VARGROUPS, SHEET_NAME_VARGROUPS, FILENAME_COUNTRYGROUPS, SHEET_NAME_COUNTRYGROUPS


def get_vargroups_from_xls(filename=FILENAME_VARGROUPS, sheet_name=SHEET_NAME_VARGROUPS):
    df = pd.read_excel(filename, sheet_name=sheet_name)
    group_list = df['Group - Code'].unique().tolist()
    groups = {}
    for group in group_list:
        groups[group] = df.loc[df['Group - Code'] == group]['Element - AMECO'].tolist()
    return groups


def get_countrygroups_from_xls(filename=FILENAME_COUNTRYGROUPS, sheet_name=SHEET_NAME_COUNTRYGROUPS):
    df = pd.read_excel(filename, sheet_name=sheet_name)
    group_list = df['Group - ISO'].unique().tolist()
    groups = {}
    for group in group_list:
        groups[group] = df.loc[df['Group - ISO'] == group]['Element - AMECO'].tolist()
    return groups
