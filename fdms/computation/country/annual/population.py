import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from fdms.config.variable_groups import TM, NA_VO, TM_TBBO, TM_TBM
from fdms.helpers.splicer import Splicer
from fdms.helpers.operators import Operators
from fdms.helpers.operators import get_series, get_scale, get_frequency



class Population:
    source_df = pd.DataFrame()

    def perform_computation(self, df, ameco_df):
        result = pd.DataFrame()
        splicer = Splicer()
        # Total labour force (unemployed + employed)
        variable = 'NLTN.1.0.0.0'
        unemployed = 'NUTN.1.0.0.0'
        employed = 'NETN.1.0.0.0'
        country = 'BE'
        base_series = get_series(ameco_df, country, variable)
        splice_series = get_series(df, country, unemployed) + get_series(df, country, employed)
        NLTN1000_meta = {'Country Ameco': country, 'Variable Code': variable,
                         'Frequency': get_frequency(df, country, employed), 'Scale': get_scale(df, country, employed)}
        NLTN1000_data = splicer.ratio_splice(base_series, splice_series, kind='forward')
        NLTN1000 = pd.Series(NLTN1000_meta)
        NLTN1000 = NLTN1000.append(NLTN1000_data)
        result = result.append(NLTN1000, ignore_index=True)

        # Self employed (employed - wage and salary earners)
        variable = 'NSTD.1.0.0.0'
        employed = 'NETN.1.0.0.0'
        salary_earners = 'NWTD.1.0.0.0'
        country = 'BE'
        base_series = get_series(ameco_df, country, variable)
        splice_series = get_series(df, country, employed) - get_series(df, country, salary_earners)
        NSTD1000_meta = {'Country Ameco': country, 'Variable Code': variable,
                         'Frequency': get_frequency(df, country, employed), 'Scale': get_scale(df, country, employed)}
        NSTD1000_data = splicer.ratio_splice(base_series, splice_series, kind='forward')
        NSTD1000 = pd.Series(NSTD1000_meta)
        NSTD1000 = NSTD1000.append(NSTD1000_data)
        result = result.append(NSTD1000, ignore_index=True)

        # Percentage employed (total employed / population of working age (15-64)
        variable = 'NETD.1.0.414.0'
        employed = 'NETD.1.0.0.0'
        working_age = 'NPAN1.1.0.0.0'
        country = 'BE'
        NETD104140_meta = {'Country Ameco': country, 'Variable Code': variable,
                         'Frequency': get_frequency(df, country, employed), 'Scale': get_scale(df, country, employed)}
        NETD104140_data = get_series(df, country, employed) - get_series(df, country, working_age) * 100
        NETD104140 = pd.Series(NETD104140_meta)
        NETD104140 = NETD104140.append(NETD104140_data)
        result = result.append(NETD104140, ignore_index=True)

        # Civilian employment
        variable = 'NECN.1.0.0.0'
        employed = 'NETN.1.0.0.0'
        NECN1000_meta = {'Country Ameco': country, 'Variable Code': variable,
                           'Frequency': get_frequency(df, country, employed), 'Scale': get_scale(df, country, employed)}
        NECN1000_data = splicer.ratio_splice(get_series(ameco_df, country, variable), get_series(df, country, employed),
                                             kind='forward')
        NECN1000 = pd.Series(NECN1000_meta)
        NECN1000 = NECN1000.append(NECN1000_data)
        result = result.append(NECN1000, ignore_index=True)

        # Total annual hours worked
        variable = 'NLHT.1.0.0.0'
        average_hours = 'NLHA.1.0.0.0'
        employed = 'NETD.1.0.0.0'
        total_hours_data = get_series(df, country, employed) * get_series(df, country, average_hours)
        NLHT1000_meta = {
            'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'Millions'}
        NLHT1000_data = splicer.ratio_splice(get_series(ameco_df, country, variable), total_hours_data, kind='forward')
        NLHT1000 = pd.Series(NLHT1000_meta)
        NLHT1000 = NLHT1000.append(NLHT1000_data)
        result = result.append(NLHT1000, ignore_index=True)

        # Total annual hours worked; total economy. for internal use only
        variable = 'NLHT9.1.0.0.0'
        average_hours = 'NLHA.1.0.0.0'
        employed = 'NETD.1.0.0.0'
        total_hours_data = get_series(df, country, employed) * get_series(df, country, average_hours)
        NLHT91000_meta = {
            'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'Millions'}
        NLHT91000_data = splicer.ratio_splice(get_series(ameco_df, country, variable), total_hours_data, kind='forward')
        NLHT91000 = pd.Series(NLHT91000_meta)
        NLTN91000 = NLHT91000.append(NLHT91000_data)
        result = result.append(NLHT91000, ignore_index=True)

        # Civilian labour force
        variable = 'NLCN.1.0.0.0'
        civilian_employment = 'NECN.1.0.0.0'
        unemployed = 'NUTN.1.0.0.0'
        NLCN1000_meta = {
            'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'Thousands'}
        NLCN1000_data = splicer.ratio_splice(get_series(ameco_df, country, variable),
                                             NECN1000_data + get_series(df, country, unemployed), kind='forward')
        NLCN1000 = pd.Series(NLCN1000_meta)
        NLCN1000 = NLCN1000.append(NLCN1000_data)
        result = result.append(NLCN1000, ignore_index=True)

        column_order = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1960, 1961, 1962, 1963, 1964, 1965,
                        1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981,
                        1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997,
                        1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                        2014, 2015, 2016, 2017, 2018, 2019]
        result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_data = result.copy()
        export_data = export_data.reset_index()
        writer = pd.ExcelWriter('output2.xlsx', engine='xlsxwriter')
        export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                           sheet_name='Sheet1', index=False)
        return result
