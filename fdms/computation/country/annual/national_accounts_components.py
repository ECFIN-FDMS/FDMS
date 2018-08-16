import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from fdms.helpers.splicer import Splicer
from fdms.helpers.operators import get_series


# National Accounts - Calculate additional GDP components
class GDPComponents:
    source_df = pd.DataFrame()

    def perform_computation(self, df):
        result = pd.DataFrame()
        splicer = Splicer()

        # Imports of goods and services at current prices (National accounts)
        variable = 'UMGS'
        goods = 'UMGN'
        services = 'UMSN'
        country = 'BE'
        UMGS_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UMGS_data = get_series(df, country, goods) + get_series(df, country, services)
        UMGS = pd.Series(UMGS_meta)
        UMGS = UMGS.append(UMGS_data)
        result = result.append(UMGS, ignore_index=True)

        # Exports of goods and services at current prices (National accounts)
        variable = 'UXGS'
        goods = 'UXGN'
        services = 'UXSN'
        country = 'BE'
        UXGS_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UXGS_data = get_series(df, country, goods) + get_series(df, country, services)
        UXGS = pd.Series(UXGS_meta)
        UXGS = UXGS.append(UXGS_data)
        result = result.append(UXGS, ignore_index=True)

        # Net exports of goods at current prices (National accounts)
        variable = 'UBGN'
        export_goods = 'UXGN'
        import_goods = 'UMGN'
        country = 'BE'
        UBGN_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UBGN_data = get_series(df, country, export_goods) - get_series(df, country, import_goods)
        UBGN = pd.Series(UBGN_meta)
        UBGN = UBGN.append(UBGN_data)
        result = result.append(UBGN, ignore_index=True)

        # Net exports of services at current prices (National accounts)
        variable = 'UBSN'
        export_services = 'UXSN'
        import_services = 'UMSN'
        country = 'BE'
        UBSN_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UBSN_data = get_series(df, country, export_services) - get_series(df, country, import_services)
        UBSN = pd.Series(UBSN_meta)
        UBSN = UBSN.append(UBSN_data)
        result = result.append(UBSN, ignore_index=True)

        # Net exports of goods and services at current prices (National accounts)
        variable = 'UBGS'
        exportgs = 'UXGS'
        importgs = 'UMGS'
        country = 'BE'
        UBGS_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UBGS_data = UXGS_data - UMGS_data
        UBGS = pd.Series(UBGS_meta)
        UBGS = UBGS.append(UBGS_data)
        result = result.append(UBGS, ignore_index=True)

        # Gross fixed capital formation at current prices: general government
        variable = 'UIGG'
        grossfcf = 'UIGG0'
        country = 'BE'
        UIGG_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UIGG_data = get_series(df, country, grossfcf)
        UIGG = pd.Series(UIGG_meta)
        UIGG = UIGG.append(UIGG_data)
        result = result.append(UIGG, ignore_index=True)

        # Gross fixed capital formation at current prices: private sector
        variable = 'UIGP'
        total = 'UIGT'
        government = 'UIGG'
        country = 'BE'
        UIGP_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UIGP_data = get_series(df, country, total) - UIGG_data
        UIGP = pd.Series(UIGP_meta)
        UIGP = UIGP.append(UIGP_data)
        result = result.append(UIGP, ignore_index=True)

        # Gross fixed capital formation at current prices: other construction
        variable = 'UIGNR'
        construction = 'UIGCO'
        dwellings = 'UIGDW'
        country = 'BE'
        UIGNR_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UIGNR_data = get_series(df, country, construction) - get_series(df, country, dwellings)
        UIGNR = pd.Series(UIGNR_meta)
        UIGNR = UIGNR.append(UIGNR_data)
        result = result.append(UIGNR, ignore_index=True)

        # Domestic demand excluding stocks at current prices
        variable = 'UUNF'
        private_consumption = 'UCPH'
        government = 'UCTG'
        total = 'UIGT'
        country = 'BE'
        UUNF_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UUNF_data = get_series(df, country, private_consumption) + get_series(df, country, total) + get_series(
            df, country, government)
        UUNF = pd.Series(UUNF_meta)
        UUNF = UUNF.append(UUNF_data)
        result = result.append(UUNF, ignore_index=True)

        # Domestic demand including stocks at current prices
        variable = 'UUNT'
        private_consumption = 'UCPH'
        government = 'UCTG'
        total = 'UIGT'
        changes = 'UIST'
        country = 'BE'
        UUNT_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UUNT_data = get_series(df, country, private_consumption) + get_series(df, country, total) + get_series(
            df, country, government) + get_series(df, country, changes)
        UUNT = pd.Series(UUNT_meta)
        UUNT = UUNT.append(UUNT_data)
        result = result.append(UUNT, ignore_index=True)

        # Final demand at current prices
        variable = 'UUTT'
        private_consumption = 'UCPH'
        government = 'UCTG'
        total = 'UIGT'
        changes = 'UIST'
        export_goods = 'UXGN'
        export_services = 'UXSN'
        country = 'BE'
        UUTT_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UUTT_data = get_series(df, country, private_consumption) + get_series(df, country, total) + get_series(
            df, country, government) + get_series(df, country, changes) + get_series(
            df, country, export_goods) + get_series(df, country, export_services)
        UUTT = pd.Series(UUTT_meta)
        UUTT = UUTT.append(UUTT_data)
        result = result.append(UUTT, ignore_index=True)

        # Gross capital formation at current prices: total economy
        variable = 'UITT'
        total = 'UIGT'
        changes = 'UIST'
        country = 'BE'
        UITT_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UITT_data = get_series(df, country, total) + get_series(df, country, changes)
        UITT = pd.Series(UITT_meta)
        UITT = UITT.append(UITT_data)
        result = result.append(UITT, ignore_index=True)

        column_order = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1960, 1961, 1962, 1963, 1964, 1965,
                        1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981,
                        1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997,
                        1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                        2014, 2015, 2016, 2017, 2018, 2019]
        result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_data = result.copy()
        export_data = export_data.reset_index()
        writer = pd.ExcelWriter('output3.xlsx', engine='xlsxwriter')
        export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                           sheet_name='Sheet1', index=False)
        return result


# National Accounts (Value) - calculate additional components
class AdditionalComponents:
    source_df = pd.DataFrame()

    def perform_computation(self, df):
        result = pd.DataFrame()
        splicer = Splicer()

        # Imports of goods and services at current prices (National accounts)
        variable = 'UMGS.1.0.0.0'
        goods = 'UMGN.1.0.0.0'
        services = 'UMSN.1.0.0.0'
        country = 'BE'
        UMGS1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UMGS1000_data = get_series(df, country, goods) + get_series(df, country, services)
        UMGS1000 = pd.Series(UMGS1000_meta)
        UMGS1000 = UMGS1000.append(UMGS1000_data)
        result = result.append(UMGS1000, ignore_index=True)

        # Exports of goods and services at current prices (National accounts)
        variable = 'UXGS.1.0.0.0'
        goods = 'UXGN.1.0.0.0'
        services = 'UXSN.1.0.0.0'
        country = 'BE'
        UXGS1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UXGS1000_data = get_series(df, country, goods) + get_series(df, country, services)
        UXGS1000 = pd.Series(UXGS1000_meta)
        UXGS1000 = UXGS1000.append(UXGS1000_data)
        result = result.append(UXGS1000, ignore_index=True)

        # Net exports of goods at current prices (National accounts)
        variable = 'UBGN.1.0.0.0'
        export_goods = 'UXGN'
        import_goods = 'UMGN'
        country = 'BE'
        UBGN1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UBGN1000_data = get_series(df, country, export_goods) - get_series(df, country, import_goods)
        UBGN1000 = pd.Series(UBGN1000_meta)
        UBGN1000 = UBGN1000.append(UBGN1000_data)
        result = result.append(UBGN1000, ignore_index=True)

        # Net exports of services at current prices (National accounts)
        variable = 'UBSN.1.0.0.0'
        export_services = 'UXSN.1.0.0.0'
        import_services = 'UMSN.1.0.0.0'
        country = 'BE'
        UBSN1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UBSN1000_data = get_series(df, country, export_services) - get_series(df, country, import_services)
        UBSN1000 = pd.Series(UBSN1000_meta)
        UBSN1000 = UBSN1000.append(UBSN1000_data)
        result = result.append(UBSN1000, ignore_index=True)

        # Net exports of goods and services at current prices (National accounts)
        variable = 'UBGS.1.0.0.0'
        exportgs = 'UXGS.1.0.0.0'
        importgs = 'UMGS.1.0.0.0'
        country = 'BE'
        UBGS1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UBGS1000_data = UXGS1000_data - UMGS1000_data
        UBGS1000 = pd.Series(UBGS1000_meta)
        UBGS1000 = UBGS1000.append(UBGS1000_data)
        result = result.append(UBGS1000, ignore_index=True)

        # Gross fixed capital formation at current prices: general government
        variable = 'UIGG.1.0.0.0'
        grossfcf = 'UIGG0.1.0.0.0'
        country = 'BE'
        UIGG1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UIGG1000_data = get_series(df, country, grossfcf)
        UIGG1000 = pd.Series(UIGG1000_meta)
        UIGG1000 = UIGG1000.append(UIGG1000_data)
        result = result.append(UIGG1000, ignore_index=True)

        # Gross fixed capital formation at current prices: private sector
        variable = 'UIGP.1.0.0.0'
        total = 'UIGT.1.0.0.0'
        government = 'UIGG.1.0.0.0'
        country = 'BE'
        UIGP1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UIGP1000_data = get_series(df, country, total) - UIGG1000_data
        UIGP1000 = pd.Series(UIGP1000_meta)
        UIGP1000 = UIGP1000.append(UIGP1000_data)
        result = result.append(UIGP1000, ignore_index=True)

        # Gross fixed capital formation at current prices: other construction
        variable = 'UIGNR.1.0.0.0'
        construction = 'UIGCO.1.0.0.0'
        dwellings = 'UIGDW.1.0.0.0'
        country = 'BE'
        UIGNR1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UIGNR1000_data = get_series(df, country, construction) - get_series(df, country, dwellings)
        UIGNR1000 = pd.Series(UIGNR1000_meta)
        UIGNR1000 = UIGNR1000.append(UIGNR1000_data)
        result = result.append(UIGNR1000, ignore_index=True)

        # Domestic demand excluding stocks at current prices
        variable = 'UUNF.1.0.0.0'
        private_consumption = 'UCPH.1.0.0.0'
        government = 'UCTG.1.0.0.0'
        total = 'UIGT.1.0.0.0'
        country = 'BE'
        UUNF1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UUNF1000_data = get_series(df, country, private_consumption) + get_series(df, country, total) + get_series(
            df, country, government)
        UUNF1000 = pd.Series(UUNF1000_meta)
        UUNF1000 = UUNF1000.append(UUNF1000_data)
        result = result.append(UUNF1000, ignore_index=True)

        # Domestic demand including stocks at current prices
        variable = 'UUNT.1.0.0.0'
        private_consumption = 'UCPH.1.0.0.0'
        government = 'UCTG.1.0.0.0'
        total = 'UIGT.1.0.0.0'
        changes = 'UIST.1.0.0.0'
        country = 'BE'
        UUNT1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UUNT1000_data = get_series(df, country, private_consumption) + get_series(df, country, total) + get_series(
            df, country, government) + get_series(df, country, changes)
        UUNT1000 = pd.Series(UUNT1000_meta)
        UUNT1000 = UUNT1000.append(UUNT1000_data)
        result = result.append(UUNT1000, ignore_index=True)

        # Final demand at current prices
        variable = 'UUTT.1.0.0.0'
        private_consumption = 'UCPH.1.0.0.0'
        government = 'UCTG.1.0.0.0'
        total = 'UIGT.1.0.0.0'
        changes = 'UIST.1.0.0.0'
        export_goods = 'UXGN.1.0.0.0'
        export_services = 'UXSN.1.0.0.0'
        country = 'BE'
        UUTT1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UUTT1000_data = get_series(df, country, private_consumption) + get_series(df, country, total) + get_series(
            df, country, government) + get_series(df, country, changes) + get_series(
            df, country, export_goods) + get_series(df, country, export_services)
        UUTT1000 = pd.Series(UUTT1000_meta)
        UUTT1000 = UUTT1000.append(UUTT1000_data)
        result = result.append(UUTT1000, ignore_index=True)

        # Gross capital formation at current prices: total economy
        variable = 'UITT.1.0.0.0'
        total = 'UIGT.1.0.0.0'
        changes = 'UIST.1.0.0.0'
        country = 'BE'
        UITT1000_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual', 'Scale': 'billions'}
        UITT1000_data = get_series(df, country, total) + get_series(df, country, changes)
        UITT1000 = pd.Series(UITT1000_meta)
        UITT1000 = UITT1000.append(UITT1000_data)
        result = result.append(UITT1000, ignore_index=True)

        column_order = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1960, 1961, 1962, 1963, 1964, 1965,
                        1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981,
                        1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997,
                        1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                        2014, 2015, 2016, 2017, 2018, 2019]
        result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_data = result.copy()
        export_data = export_data.reset_index()
        writer = pd.ExcelWriter('output4.xlsx', engine='xlsxwriter')
        export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                           sheet_name='Sheet1', index=False)
        return result
