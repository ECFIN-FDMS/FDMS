import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd
import re

from fdms.config.variable_groups import NA_VO
from fdms.config.country_groups import FCWVACP
from fdms.helpers.splicer import Splicer
from fdms.helpers.operators import Operators
from fdms.helpers.operators import get_series, get_scale, get_frequency


class NationalAccountsVolume:
    source_df = pd.DataFrame()
    country = 'BE'
    splicer = Splicer()
    result = pd.DataFrame()

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
        result = self.result.append(series, ignore_index=True, sort=True)

    def perform_computation(self, df, ameco_df=None):
        ameco_df = ameco_df if ameco_df is not None else df
        result = pd.DataFrame()
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
                    result.append(new_series)
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
                    result.append(new_series, ignore_index=True)

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
                    # series = pd.Series(series_meta)
                    # series = series.append(series_data)
                    # result = result.append(series, ignore_index=True, sort=True)

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
            base_series = pd.to_numeric(get_series(df, self.country, ameco_exports)) - pd.to_numeric(
                get_series(df, self.country, ameco_imports))
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
            base_series = pd.to_numeric(get_series(df, self.country, ameco_1)) - pd.to_numeric(
                get_series(df, self.country, ameco_2))
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
            u_series = pd.to_numeric(get_series(df, self.country, u_new_private_consumption)) + pd.to_numeric(
                get_series(df, self.country, u_new_government_consumption)) + pd.to_numeric(get_series(
                df, self.country, u_new_use))
            base_series = pd.to_numeric(get_series(df, self.country, private_consumption)) + pd.to_numeric(get_series(
                df, self.country, government_consumption)) + pd.to_numeric(get_series(df, self.country, use_ameco))
            splice_series_1 = pd.to_numeric(get_series(df, self.country, new_private_consumption)) + pd.to_numeric(
                get_series(df, self.country, new_government_consumption)) + pd.to_numeric(get_series(
                df, self.country, new_use))
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
                        sum_u_series = sum(pd.to_numeric(get_series(df, self.country, v)) for v in new_vars)
                        splice_series_2 = splice_series_1.copy() / sum_u_series.shift(1) - 1 * 100
                        if splice_series_2 is not None:
                            self._update_result(var, base_series, splice_series_1, splice_series_2)
                        else:
                            logger.error('Missing data for variable {} in national accounts volume (172)'.format(
                                new_variable))
                    else:
                        self._update_result(var, base_series, splice_series_1, None)

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
                base_series = pd.to_numeric(get_series(df, self.country, variables[
                    'exports'][counter])) - pd.to_numeric(get_series(df, self.country, variables['imports'][counter]))
                splice_series_1 = get_series(df, self.country, variables['new_exports'][counter]) - get_series(
                    df, self.country, variables['new_imports'][counter])
                if self.country in FCWVACP:
                    u_series = get_series(df, self.country, variables['u_exports']) - get_series(df, self.country, variables['u_services'])
                    splice_series_2 = splice_series_1 / u_series.shift(1) - 1 * 100
                return base_series, splice_series_1, splice_series_2

