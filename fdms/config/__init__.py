import os
import re


DEFAULT_COUNTRY = 'BE'
COUNTRY = os.environ.get('DMS_COUNTRY') or DEFAULT_COUNTRY
AMECO = 'fdms/sample_data/AMECO_H.TXT'
FORECAST = 'fdms/sample_data/LT.Forecast.SF2018.xlsm'
FORECAST = 'fdms/sample_data/{}.Forecast.0908.xlsm'.format(COUNTRY)
AMECO_SHEET = COUNTRY
COUNTRY_CALCULATION_TXT = 'fdms/utils/country_calculation.txt'

BASE_PERIOD = 2010

FILENAME_VARGROUPS = 'fdms/sample_data/vargroups.xlsx'
SHEET_NAME_VARGROUPS = 'vargroups'
FILENAME_COUNTRYGROUPS = 'fdms/sample_data/countrygroups.xlsx'
SHEET_NAME_COUNTRYGROUPS = 'countrygroups'

VARS_FILENAME = 'output/outputvars.txt'
EXCEL_FILENAME = 'output/output.xlsx'
COLUMN_ORDER = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000,
                2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017,
                2018, 2019]
YEARS = [year for year in COLUMN_ORDER if re.match('^\d{4}$', str(year))]
LAST_YEAR = YEARS[-1]
FIRST_YEAR = YEARS[0]
