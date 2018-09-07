import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd
import re

from fdms.config.variable_groups import NA_VO
from fdms.config.country_groups import FCWVACP
from fdms.utils.splicer import Splicer
from fdms.utils.operators import Operators
from fdms.utils.operators import get_series, get_scale, get_frequency


# TODO: Create config file
BASE_PERIOD = 2010


class NationalAccountsVolume:
    result = pd.DataFrame()
    country = 'BE'
    frequency = 'Annual'
    splicer = Splicer()

    def _update_result(self, variable, base_series, splice_series_1, splice_series_2, frequency='Annual',
                      scale='billions'):
        if self.country in FCWVACP:
            series_data = self.splicer.ratio_splice(base_series, splice_series_1, kind='forward')
        else:
            if splice_series_2 is not None:
                series_data = self.splicer.splice_and_level_forward(base_series, splice_series_2, kind='forward')
            else:
                logger.error('Missing data for variable {} in national accounts volume'.format(variable))
                return
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': frequency, 'Scale': scale}
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

    def _get_data(self, group_number, variables, df=None):
        splice_series_2 = None
        for counter, variable in enumerate(variables['variables']):
            if group_number == 1:
                base_series = get_series(df, self.country, variables['ameco'][counter])
                splice_series_1 = get_series(df, self.country, variables['goods'][counter]) + get_series(
                    df, self.country, variables['services'][counter])
                if self.country in FCWVACP:
                    u_series = get_series(df, self.country, variables['u_goods'][counter]) + get_series(
                        df, self.country, variables['u_services'][counter])
                    splice_series_2 = splice_series_1 / u_series.shift(1) - 1 * 100
                # RatioSplice(base, level(series)) = base * (1 + 0,01 * series)
            elif group_number == 2:
                base_series = get_series(df, self.country, variables['exports'][counter]) - get_series(
                    df, self.country, variables['imports'][counter])
                splice_series_1 = get_series(df, self.country, variables['new_exports'][counter]) - get_series(
                    df, self.country, variables['new_imports'][counter])
                if self.country in FCWVACP:
                    u_series = get_series(df, self.country, variables['u_exports']) - get_series(df, self.country, variables['u_services'])
                    splice_series_2 = splice_series_1 / u_series.shift(1) - 1 * 100
                return base_series, splice_series_1, splice_series_2

    def perform_computation(self, df, ameco_df=None):
        ameco_df = ameco_df if ameco_df is not None else df
        for index, row in df.iterrows():
            country = index[0]
            self.country = country
            variable = index[1]
            new_variable = variable + '.1.0.0.0'
            u_variable = re.sub('^.', 'U', variable)
            variable11 = variable + '.1.1.0.0'
            if variable in NA_VO:
                if country in FCWVACP:
                    new_data = self.splicer.ratio_splice(get_series(ameco_df, country, u_variable),
                                                    get_series(df, country, variable), kind='forward')
                    new_meta = pd.Series({'Variable Code': new_variable, 'Country Ameco': country,
                                'Frequency': get_frequency(df, country, variable),
                                'Scale': get_scale(df, country, variable)})
                    new_series = new_meta.append(new_data)
                    self.result = self.result.append(new_series, ignore_index=True)
                else:
                    try:
                        series = get_series(df, country, variable)
                        u_series = get_series(df, country, u_variable)
                        series11 = get_series(df, country, variable11)
                    except KeyError:
                        logger.error('Missing data for variable {} in national accounts volume'.format(new_variable))
                        continue
                    splice_series = (series / u_series.shift(1) - 1) * 100
                    # RatioSplice(base, level(series)) = base * (1 + 0, 01 * series)
                    new_data = self.splicer.splice_and_level_forward(series11, splice_series)
                    new_meta = pd.Series({'Variable Code': new_variable, 'Country Ameco': country,
                                          'Frequency': get_frequency(df, country, variable),
                                          'Scale': get_scale(df, country, variable)})
                    new_series = new_meta.append(new_data)
                    self.result = self.result.append(new_series, ignore_index=True)

        # Imports / exports of goods and services
        group_1 = {'variables': ['OMGS.1.0.0.0', 'OXGS.1.0.0.0'], 'ameco': ['OMGS.1.1.0.0', 'OXGS.1.1.0.0'],
                   'goods': ['OMGN', 'OXGN'], 'services': ['OMSN', 'OXSN'], 'u_goods': ['UMGN,', 'UXGN'],
                   'u_services': ['UMSN,', 'UXSN']}

        # Net imports / exports of goods, services and investments
        group_2 = {
            'variables': ['OBGN.1.0.0.0', 'OBSN.1.0.0.0', 'OIGP.1.0.0.0'],
            'exports': ['OXGN.1.1.0.0', 'OXSN.1.1.0.0', 'OIGT.1.1.0.0'],
            'imports': ['OMGN.1.1.0.0', 'OMSN.1.1.0.0', 'OIGG.1.1.0.0'],
            'new_exports': ['OXGN', 'OXSN', 'OIGT'], 'new_imports': ['OMGN', 'OMGN', 'OIGG'],
            'u_exports': ['UXGN', 'UXSN', 'UIGT'], 'u_imports': ['UMGN', 'UMGN', 'UIGG']
        }

        for number, group in enumerate([group_1, group_2]):
            for counter, variable in enumerate(group['variables']):
                base_series = None
                series_meta = {'Country Ameco': country, 'Variable Code': variable, 'Frequency': 'Annual',
                               'Scale': 'billions'}
                try:
                    base_series, splice_series_1, splice_series_2 = self._get_data(number + 1, group, df)
                except TypeError:
                    logger.error('Missing data for variable {} in national accounts volume'.format(variable))
                if base_series is not None:
                    self._update_result(variable, base_series, splice_series_1, None)

        # Net exports goods and services
        var = 'OBGS.1.0.0.0'
        ameco_exports = 'OXGS.1.1.0.0'
        ameco_imports = 'OMGS.1.1.0.0'
        goods_exports = 'OXGN'
        services_exports = 'OXSN'
        goods_imports = 'OMGN'
        services_imports = 'OMSN'
        u_goods_exports = 'UXGN'
        u_services_exports = 'UXSN'
        u_goods_imports = 'UMGN'
        u_services_imports = 'UMSN'
        export_series = get_series(df, self.country, goods_exports) + get_series(df, self.country, services_exports)
        import_series = get_series(df, self.country, goods_imports) + get_series(df, self.country, services_imports)
        u_exports = get_series(df, self.country, u_goods_exports) + get_series(df, self.country, u_services_exports)
        u_imports = get_series(df, self.country, u_goods_imports) + get_series(df, self.country, u_services_imports)
        base_series = get_series(df, self.country, ameco_exports) - get_series(df, self.country, ameco_imports)
        splice_series_1 = export_series - import_series
        splice_series_2 = (export_series - import_series) / (u_exports - u_imports).shift(1) - 1 * 100
        self._update_result(var, base_series, splice_series_1, splice_series_2)

        # Investments
        var = 'OIGNR.1.0.0.0'
        ameco_1 = 'OIGCO.1.1.0.0'
        ameco_2 = 'OIGDW.1.1.0.0'
        investments_1 = 'OIGCO'
        investments_2 = 'OIGDW'
        u_investments_1 = 'UIGCO'
        u_investments_2 = 'UIGDW'
        net_series = get_series(df, self.country, investments_1) - get_series(df, self.country, investments_2)
        u_net_series = get_series(df, self.country, u_investments_1) - get_series(df, self.country, u_investments_2)
        base_series = get_series(df, self.country, ameco_1) - get_series(df, self.country, ameco_2)
        splice_series_1 = net_series.copy()
        splice_series_2 = net_series / u_net_series.shift(1) - 1 * 100
        self._update_result(var, base_series, splice_series_1, splice_series_2)

        # Domestic demand
        var = 'OUNF.1.0.0.0'
        private_consumption = 'OCPH.1.1.0.0'
        government_consumption = 'OCTG.1.1.0.0'
        use_ameco = 'OIGT.1.1.0.0'
        new_private_consumption = 'OCPH'
        new_government_consumption = 'OCTG'
        new_use = 'OIGT'
        u_new_private_consumption = 'UCPH'
        u_new_government_consumption = 'UCTG'
        u_new_use = 'UIGT'
        u_series = get_series(df, self.country, u_new_private_consumption) + get_series(
            df, self.country, u_new_government_consumption) + get_series(df, self.country, u_new_use)
        base_series = get_series(df, self.country, private_consumption) + get_series(
            df, self.country, government_consumption) + get_series(df, self.country, use_ameco)
        splice_series_1 = get_series(df, self.country, new_private_consumption) + get_series(
            df, self.country, new_government_consumption) + get_series(df, self.country, new_use)
        splice_series_2 = splice_series_1 / u_series.shift(1) - 1 * 100
        self._update_result(var, base_series, splice_series_1, splice_series_2)

        # Domestic demand
        variables = {'OUNT.1.0.0.0': ['OUNT.1.1.0.0', 'OCPH', 'OCTG', 'OIGT', 'OIST'],
                     'OUTT.1.0.0.0': ['OUTT.1.1.0.0', 'OCPH', 'OCTG', 'OIGT', 'OIST', 'OXGN', 'OXSN'],
                     'OITT.1.0.0.0': ['OITT.1.0.0.0', 'OIGT', 'OIST']}
        for var, new_vars in variables.items():
            try:
                base_series = get_series(df, self.country, new_vars[0])
                splice_series_1 = sum([get_series(df, self.country, v) for v in new_vars[1:]])
            except KeyError:
                logger.error('Missing data for variable {} in national accounts volume (172)'.format(var))
            else:
                splice_series_2 = None
                if self.country not in FCWVACP:
                    u_new_vars = [re.sub('^.', 'U', v) for v in new_vars[1:]]
                    sum_u_series = sum(get_series(df, self.country, v) for v in new_vars)
                    splice_series_2 = splice_series_1.copy() / sum_u_series.shift(1) - 1 * 100
                    if splice_series_2 is not None:
                        self._update_result(var, base_series, splice_series_1, splice_series_2)
                    else:
                        logger.error('Missing data for variable {} in national accounts volume (172)'.format(
                            new_variable))
                else:
                    self._update_result(var, base_series, splice_series_1, None)

        # Volume, rebase to baseperiod, percent change, contribution to percent change in GDP
        for var in NA_VO:
            new_variable = var + '.1.0.0.0'
            u1_variable = re.sub('^.', 'U', var) + '.1.0.0.0'

            if new_variable in self.result['Variable Code'].values:
                result_series_index = self.result.loc[(self.result['Country Ameco'] == self.country) & (
                        self.result['Variable Code'] == new_variable)].index.values[0]
                series_orig = self.result.loc[result_series_index]
                data_orig = pd.to_numeric(series_orig.filter(regex='\d{4}'), errors='coerce')

                # Rebase to baseperiod
                if u1_variable in df.index.get_level_values('Variable Code'):
                    series_meta = {'Country Ameco': series_orig['Country Ameco'], 'Variable Code': new_variable,
                                   'Frequency': series_orig['Frequency'], 'Scale': series_orig['Scale']}
                    u1_series = get_series(df, self.country, u1_variable)
                    value_to_rebase = data_orig[BASE_PERIOD] / u1_series[BASE_PERIOD]
                    series_data = data_orig * value_to_rebase
                    series = pd.Series(series_meta)
                    series = series.append(series_data)
                    self.result.iloc[result_series_index] = series
                else:
                    logger.error('Missing data for variable {} in national accounts volume'.format(u1_variable))

                # Percent change
                variable_6 = var + '.6.0.0.0'
                series_meta = {'Country Ameco': self.country, 'Variable Code': variable_6,
                               'Frequency': series_orig['Frequency'], 'Scale': 'units'}
                series_data = data_orig.pct_change()
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

                # Contribution to percent change in GDP
                variable_c1 = re.sub('^.', 'C', var) + '.1.0.0.0'
                variable_x = new_variable if self.country in ['MT', 'TR'] else u1_variable
                series_6_index = self.result.loc[(self.result['Country Ameco'] == self.country) & (
                        self.result['Variable Code'] == variable_6)].index.values[0]
                series_6 = self.result.loc[result_series_index]
                data_6 = pd.to_numeric(series_6.filter(regex='\d{4}'), errors='coerce')
                xvgd = 'OVGD.1.0.0.0' if self.country in ['MT', 'TR'] else 'UVGD.1.0.0.0'
                series_meta = {'Country Ameco': self.country, 'Variable Code': variable_c1,
                               'Frequency': series_6['Frequency'], 'Scale': 'units'}
                series_data = data_6 * get_series(df, self.country, variable_x).shift(1) / get_series(
                    df, self.country, xvgd).shift(1)
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

            else:
                logger.error('Missing data for variable {} in national accounts volume'.format(new_variable))

            # Contribution to percent change in GDP (calculation for additional variables)
            # Variables needed for the rest of calculations:
            # TODO: Data for the rest is missing, let's merge this as it is and work on the interfaces
            # That way it'll be easier to track

            # Per-capita GDP

            # Terms of trade

            # Set up OVGD.6.1.212.0 for World GDP volume table

            # Convert percent change of trade variables (volume) from national currency to USD

            column_order = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1993, 1994, 1995, 1996, 1997,
                            1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                            2014, 2015, 2016, 2017, 2018, 2019]
            self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
            export_data = self.result.copy()
            export_data = export_data.reset_index()
            writer = pd.ExcelWriter('output4.xlsx', engine='xlsxwriter')
            export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                               sheet_name='Sheet1', index=False)
            return self.result

