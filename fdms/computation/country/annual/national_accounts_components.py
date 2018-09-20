import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from fdms.utils.splicer import Splicer
from fdms.utils.series import get_series


# National Accounts - Calculate additional GDP components
class GDPComponents:
    source_df = pd.DataFrame()

    def perform_computation(self, df):
        result = pd.DataFrame()
        splicer = Splicer()

        # Imports and exports of goods and services at current prices (National accounts)
        variables = ['UMGS', 'UXGS', 'UMGS.1.0.0.0', 'UXGS.1.0.0.0']
        goods = ['UMGN', 'UXGN', 'UMGN.1.0.0.0', 'UXGN.1.0.0.0']
        services = ['UMSN', 'UXSN', 'UMSN.1.0.0.0', 'UXSN.1.0.0.0']
        country = 'BE'
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = get_series(df, country, goods[index]).astype(float) + get_series(
                df, country, services[index]).astype(float)
            series = pd.Series(series_meta)
            series = series.append(series_data)
            result = result.append(series, ignore_index=True, sort=True)

        # Gross fixed capital formation at current prices: general government
        variables = ['UIGG', 'UIGG.1.0.0.0']
        grossfcf = ['UIGG0', 'UIGG0.1.0.0.0']
        country = 'BE'
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = get_series(df, country, grossfcf[index])
            series = pd.Series(series_meta)
            series = series.append(series_data)
            result = result.append(series, ignore_index=True, sort=True)

        # Net exports of goods, services, and goods & services at current prices (National accounts)
        # TODO: Check that the 4th variable is correct in exports_goods_and_services and imports_goods_and_services
        variables = ['UBGN', 'UBSN', 'UBGS', 'UBGN.1.0.0.0', 'UBSN.1.0.0.0', 'UBGS.1.0.0.0', 'UIGP', 'UIGNR',
                     'UIGP.1.0.0.0', 'UIGNR.1.0.0.0']
        exports_goods_and_services = ['UXGN', 'UXSN', 'UXGS', 'UXGN', 'UXSN.1.0.0.0', 'UXGS.1.0.0.0', 'UIGT', 'UIGCO',
                                      'UIGT.1.0.0.0', 'UIGCO.1.0.0.0']
        imports_goods_and_services = ['UMGN', 'UMSN', 'UMGS', 'UMGN', 'UMSN.1.0.0.0', 'UMGS.1.0.0.0', 'UIGG', 'UIGDW',
                                      'UIGG.1.0.0.0', 'UIGDW.1.0.0.0']
        country = 'BE'
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            try:
                exports_data = get_series(df, country, exports_goods_and_services[index])
            except KeyError:
                exports_data = result.loc[result['Variable Code'] == exports_goods_and_services[index]].filter(
                    regex='^\d{4}$')
            try:
                imports_data = get_series(df, country, imports_goods_and_services[index])
            except KeyError:
                imports_data = result.loc[result['Variable Code'] == imports_goods_and_services[index]].filter(
                    regex='^\d{4}$')
            if type(exports_data) == pd.DataFrame:
                exports_data = exports_data.iloc[0]
            if type(imports_data) == pd.DataFrame:
                imports_data = imports_data.iloc[0]
            if not isinstance(exports_data.name, type(imports_data.name)):
                imports_data.name = None
            try:
                series_data = exports_data.astype(float) - imports_data.astype(float)
            except ValueError:
                series_data = exports_data - imports_data
            series = pd.Series(series_meta)
            series = series.append(series_data)
            result = result.append(series, ignore_index=True, sort=True)

        # Domestic demand excluding stocks at current prices
        variables = ['UUNF', 'UUNF.1.0.0.0']
        private_consumption = ['UCPH', 'UCPH.1.0.0.0']
        government = ['UCTG', 'UCTG.1.0.0.0']
        total = ['UIGT', 'UIGT.1.0.0.0']
        country = 'BE'
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = get_series(df, country, private_consumption[index]) + get_series(
                df, country, total[index]) + get_series(df, country, government[index])
            series = pd.Series(series_meta)
            series = series.append(series_data)
            result = result.append(series, ignore_index=True, sort=True)

        # Domestic demand including stocks at current prices
        variables = ['UUNT', 'UUNT.1.0.0.0']
        private_consumption = ['UCPH', 'UCPH.1.0.0.0']
        government = ['UCTG', 'UCTG.1.0.0.0']
        total = ['UIGT', 'UIGT.1.0.0.0']
        changes = ['UIST', 'UIST.1.0.0.0']
        country = 'BE'
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = get_series(df, country, private_consumption[index]) + get_series(df, country, total[
                index]) + get_series(df, country, government[index]) + get_series(df, country, changes[index])
            series = pd.Series(series_meta)
            series = series.append(series_data)
            result = result.append(series, ignore_index=True, sort=True)

        # Final demand at current prices
        variables = ['UUTT', 'UUTT.1.0.0.0']
        private_consumption = ['UCPH', 'UCPH.1.0.0.0']
        government = ['UCTG', 'UCTG.1.0.0.0']
        total = ['UIGT', 'UIGT.1.0.0.0']
        changes = ['UIST', 'UIST.1.0.0.0']
        export_goods = ['UXGN', 'UXGN.1.0.0.0']
        export_services = ['UXSN', 'UXSN.1.0.0.0']
        country = 'BE'
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = get_series(df, country, private_consumption[index]) + get_series(df, country, total[
                index]) + get_series(df, country, government[index]) + get_series(df, country, changes[
                index]) + get_series(df, country, export_goods[index]) + get_series(df, country, export_services[index])
            series = pd.Series(series_meta)
            series = series.append(series_data)
            result = result.append(series, ignore_index=True, sort=True)

        # Gross capital formation at current prices: total economy
        variables = ['UITT', 'UITT.1.0.0.0']
        total = ['UIGT', 'UIGT.1.0.0.0']
        changes = ['UIST', 'UIST.1.0.0.0']
        country = 'BE'
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'billions'}
            series_data = get_series(df, country, total[index]) + get_series(df, country, changes[index])
            series = pd.Series(series_meta)
            series = series.append(series_data)
            result = result.append(series, ignore_index=True, sort=True)

        column_order = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1993, 1994, 1995, 1996, 1997,
                        1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                        2014, 2015, 2016, 2017, 2018, 2019]
        result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_data = result.copy()
        export_data = export_data.reset_index()
        writer = pd.ExcelWriter('output/output3.xlsx', engine='xlsxwriter')
        export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                           sheet_name='Sheet1', index=False)
        result_vars = result.index.get_level_values('Variable Code').tolist()
        with open('output/outputvars3.txt', 'w') as f:
            f.write('\n'.join(result_vars))
        return result

