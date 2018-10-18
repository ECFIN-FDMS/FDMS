import logging

from fdms.utils.mixins import StepMixin

logging.basicConfig(filename='error.log',
                    format='{%(pathname)s:%(lineno)d} - %(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd
import re

from fdms.config.variable_groups import NA_VO, T_VO
from fdms.config.country_groups import FCWVACP
from fdms.utils.splicer import Splicer
from fdms.config import BASE_PERIOD
from fdms.utils.series import get_series, get_series_noindex, get_index, get_scale, get_frequency, export_to_excel


# STEP 4
class NationalAccountsVolume(StepMixin):
    splicer = Splicer()

    def _update_result(self, variable, base_series, splice_series_1, splice_series_2, frequency='Annual',
                       scale='Billions'):
        if self.country in FCWVACP:
            series_data = self.splicer.ratio_splice(base_series, splice_series_1, kind='forward')
        else:
            if splice_series_2 is not None:
                series_data = self.splicer.splice_and_level_forward(base_series, splice_series_2, kind='forward',
                                                                    variable=variable)
            else:
                logger.error('Missing data for variable {} in national accounts volume'.format(variable))
                return
        series_meta = self.get_meta(variable)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

    def _get_data(self, group_number, variables, df=None, ameco_df=None):
        splice_series_2 = None
        for counter, variable in enumerate(variables['variables']):
            if group_number == 1:
                base_series = get_series(ameco_df, self.country, variables['ameco'][counter])
                splice_series_1 = get_series(df, self.country, variables['goods'][counter]) + get_series(
                    df, self.country, variables['services'][counter])
                if self.country not in FCWVACP:
                    u_series = get_series(df, self.country, variables['u_goods'][counter]) + get_series(
                        df, self.country, variables['u_services'][counter])
                    splice_series_2 = (splice_series_1 / u_series.shift(1) - 1) * 100
                # RatioSplice(base, level(series)) = base * (1 + 0,01 * series)
            elif group_number == 2:
                base_series = get_series(ameco_df, self.country, variables['exports'][counter]) - get_series(
                    ameco_df, self.country, variables['imports'][counter])
                splice_series_1 = get_series(df, self.country, variables['new_exports'][counter]) - get_series(
                    df, self.country, variables['new_imports'][counter])
                if self.country not in FCWVACP:
                    u_series = get_series(df, self.country, variables['u_exports'][counter]) - get_series(
                        df, self.country, variables['u_imports'][counter])
                    splice_series_2 = (splice_series_1 / u_series.shift(1) - 1) * 100
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
                    new_meta = pd.Series(self.get_meta(new_variable))
                    new_series = new_meta.append(new_data)
                    self.result = self.result.append(new_series, ignore_index=True)
                else:
                    series = get_series(df, country, variable)
                    u_series = get_series(df, country, u_variable)
                    try:
                        series11 = get_series(ameco_df, country, variable11)
                    except KeyError:
                        logger.warning('Missing Ameco data for variable {} (national accounts volume). Using data '
                                       'from country desk forecast'.format(variable11))
                    splice_series = (series / u_series.shift(1) - 1) * 100
                    # RatioSplice(base, level(series)) = base * (1 + 0,01 * series)
                    new_data = self.splicer.splice_and_level_forward(series11, splice_series)
                    new_meta = pd.Series(self.get_meta(new_variable))
                    new_series = new_meta.append(new_data)
                    self.result = self.result.append(new_series, ignore_index=True)

        # Imports / exports of goods and services
        group_1 = {'variables': ['OMGS.1.0.0.0', 'OXGS.1.0.0.0'], 'ameco': ['OMGS.1.1.0.0', 'OXGS.1.1.0.0'],
                   'goods': ['OMGN', 'OXGN'], 'services': ['OMSN', 'OXSN'], 'u_goods': ['UMGN', 'UXGN'],
                   'u_services': ['UMSN', 'UXSN']}

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
                series_meta = self.get_meta(variable)
                try:
                    base_series, splice_series_1, splice_series_2 = self._get_data(number + 1, group, df, ameco_df)
                except TypeError:
                    logger.error('Missing data for variable {} in national accounts volume'.format(variable))
                # if variable == 'OXGS.1.0.0.0':
                #     import code;code.interact(local=locals())
                self._update_result(variable, base_series, splice_series_1, splice_series_2)

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
        base_series = get_series(ameco_df, self.country, ameco_exports) - get_series(ameco_df, self.country, ameco_imports)
        splice_series_1 = export_series - import_series
        splice_series_2 = ((export_series - import_series) / (u_exports - u_imports).shift(1) - 1) * 100
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
        base_series = get_series(ameco_df, self.country, ameco_1) - get_series(ameco_df, self.country, ameco_2)
        splice_series_1 = net_series.copy()
        splice_series_2 = (net_series / u_net_series.shift(1) - 1) * 100
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
        base_series = get_series(ameco_df, self.country, private_consumption) + get_series(
            ameco_df, self.country, government_consumption) + get_series(ameco_df, self.country, use_ameco)
        splice_series_1 = get_series(df, self.country, new_private_consumption) + get_series(
            df, self.country, new_government_consumption) + get_series(df, self.country, new_use)
        splice_series_2 = (splice_series_1 / u_series.shift(1) - 1) * 100
        self._update_result(var, base_series, splice_series_1, splice_series_2)

        # Domestic demand
        variables = {'OUNT.1.0.0.0': ['OUNT.1.1.0.0', 'OCPH', 'OCTG', 'OIGT', 'OIST'],
                     'OUTT.1.0.0.0': ['OUTT.1.1.0.0', 'OCPH', 'OCTG', 'OIGT', 'OIST', 'OXGN', 'OXSN'],
                     'OITT.1.0.0.0': ['OITT.1.0.0.0', 'OIGT', 'OIST']}
        for var, new_vars in variables.items():
            base_series = None
            splice_series_1 = sum([get_series(df, self.country, v) for v in new_vars[1:]])
            try:
                base_series = get_series(df, self.country, new_vars[0])
            except KeyError:
                logger.warning('No historical data for {} to level_splice, country {}, using country forecast '
                               'data.'.format(new_vars[0], self.country))
            splice_series_2 = None
            if self.country not in FCWVACP:
                u_new_vars = [re.sub('^.', 'U', v) for v in new_vars[1:]]
                try:
                    sum_u_series = sum(get_series(df, self.country, v) for v in new_vars[1:])
                    splice_series_2 = splice_series_1.copy() / sum_u_series.shift(1) - 1 * 100
                    self._update_result(var, base_series, splice_series_1, splice_series_2)
                except KeyError:
                    logger.error('Missing data for variable {} in national accounts volume (172)'.format(
                        new_variable))
            else:
                self._update_result(var, base_series, splice_series_1, None)

        # Volume, rebase to baseperiod, percent change, contribution to percent change in GDP
        for var in NA_VO:
            new_variable = var + '.1.0.0.0'
            u1_variable = re.sub('^.', 'U', var) + '.1.0.0.0'

            if new_variable in self.result['Variable Code'].values:
                result_series_index = get_index(self.result, self.country, new_variable)
                series_orig = self.result.loc[result_series_index]
                data_orig = pd.to_numeric(series_orig.filter(regex='\d{4}'), errors='coerce')

                # Rebase to baseperiod
                if u1_variable in df.index.get_level_values('Variable Code'):
                    series_meta = self.get_meta(new_variable)
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
                series_meta = self.get_meta(variable_6)
                series_data = data_orig.pct_change() * 100
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

                # Contribution to percent change in GDP
                variable_c1 = re.sub('^.', 'C', var) + '.1.0.0.0'
                variable_x = new_variable if self.country in ['MT', 'TR'] else u1_variable
                series_6_index = get_index(self.result, self.country, variable_6)
                series_6 = self.result.loc[result_series_index]
                data_6 = pd.to_numeric(series_6.filter(regex='\d{4}'), errors='coerce')
                xvgd = 'OVGD.1.0.0.0' if self.country in ['MT', 'TR'] else 'UVGD.1.0.0.0'
                series_meta = self.get_meta(variable_c1)
                try:
                    series_data = data_6 * get_series(df, self.country, variable_x).shift(1) / get_series(
                        df, self.country, xvgd).shift(1)
                except KeyError:
                    logger.error('Missing data for variable {} in national accounts volume'.format(new_variable))
                    continue
                series = pd.Series(series_meta)
                series = series.append(series_data)
                self.result = self.result.append(series, ignore_index=True, sort=True)

            else:
                logger.error('Missing data for variable {} in national accounts volume'.format(new_variable))

        # Contribution to percent change in GDP (calculation for additional variables)
        var = 'CMGS.1.0.0.0'
        series_meta = self.get_meta(var)
        series_data = -get_series_noindex(self.result, self.country, var)
        index = get_index(self.result, self.country, var)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result.iloc[index] = series
        var = 'CBGS.1.0.0.0'
        exports = 'CXGS.1.0.0.0'
        imports = 'CMGS.1.0.0.0'
        series_meta = self.get_meta(var)
        series_meta['Variable Code'] = var
        series_data = get_series_noindex(self.result, self.country, exports) + get_series_noindex(
            self.result, self.country, imports)
        index = get_index(self.result, self.country, var)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        # TODO: If Country in group 'Forecast: Countries with volumes at constant prices' line 202 country calc

        # Per-capita GDP
        # TODO: fix scale, frequency and country everywhere
        new_variable = 'RVGDP.1.0.0.0'
        ameco_variable = 'RVGDP.1.1.0.0'
        variable_6 = re.sub('.1.0.0.0', '.6.0.0.0', new_variable)
        total_population = 'NPTD.1.0.0.0'
        potential_gdp = 'OVGD.1.0.0.0'
        series_meta = self.get_meta(new_variable)
        series_6_meta = self.get_meta(variable_6)
        ameco_series = get_series(ameco_df, self.country, ameco_variable)
        splice_series = get_series_noindex(self.result, self.country, potential_gdp) / get_series(
            df, self.country, total_population)
        splicer = Splicer()
        series_data = splicer.ratio_splice(ameco_series, splice_series)
        series_6_data = series_data.pct_change() * 100
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        series_6 = pd.Series(series_6_meta)
        series_6 = series_6.append(series_6_data)
        self.result = self.result.append(series_6, ignore_index=True, sort=True)
        # TODO: Do not add series if they're alreade there, i.e. df.loc['BE','UMGS'] is repeated

        # Terms of trade
        variables = ['APGN.3.0.0.0', 'APSN.3.0.0.0', 'APGS.3.0.0.0']
        exports_1 = ['UXGN.1.0.0.0', 'UXSN.1.0.0.0', 'UXGS.1.0.0.0']
        exports_2 = ['OXGN.1.0.0.0', 'OXSN.1.0.0.0', 'OXGS.1.0.0.0']
        imports_1 = ['UMGN.1.0.0.0', 'UMSN.1.0.0.0', 'UMGS.1.0.0.0']
        imports_2 = ['OMGN.1.0.0.0', 'OMSN.1.0.0.0', 'OMGS.1.0.0.0']
        for index, variable in enumerate(variables):
            series_meta = self.get_meta(variable)
            series_data = (get_series(
                df, self.country, exports_1[index]) / get_series_noindex(
                self.result, self.country, exports_2[index]) / (
                    get_series(df, self.country, imports_1[index]) / get_series_noindex(
                self.result, self.country, imports_2[index]))) * 100
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)
            variable_6 = re.sub('3', '6', variable)
            series_meta = self.get_meta(variable_6)
            series_data = series_data.pct_change() * 100
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        # Set up OVGD.6.1.212.0 for World GDP volume table
        variable = 'OVGD.6.1.212.0'
        series_meta = self.get_meta(variable)
        series_data = get_series_noindex(self.result, self.country, 'OVGD.6.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        # Convert percent change of trade variables (volume) from national currency to USD
        for variable in T_VO:
            new_variable = variable + '.6.0.30.0'
            variable_6 = variable + '.6.0.0.0'
            series_meta = self.get_meta(new_variable)
            series_data = get_series_noindex(self.result, self.country, variable_6)
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, 'output/output4.xlsx')
        return self.result

