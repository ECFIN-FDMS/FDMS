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
from fdms.utils.series import export_to_excel


# STEP 4
class NationalAccountsVolume(StepMixin):
    splicer = Splicer()

    def _update_result(self, variable, base_series, splice_series_1, splice_series_2, scale='Billions'):
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

    def _get_data(self, variable, components, df=None, ameco_df=None):
        splice_series_2 = None
        if variable in ['OMGS.1.0.0.0', 'OXGS.1.0.0.0']:
            base_series = self.get_data(ameco_df, components['ameco'])
            splice_series_1 = self.get_data(df, components['goods']) + self.get_data(df, components['services'])
            if self.country not in FCWVACP:
                u_series = self.get_data(df, components['u_goods']) + self.get_data(df, components['u_services'])
                splice_series_2 = (splice_series_1 / u_series.shift(1) - 1) * 100
            # RatioSplice(base, level(series)) = base * (1 + 0,01 * series)
        else:
            try:
                base_series = self.get_data(ameco_df, components['exports']) - self.get_data(
                    ameco_df, components['imports'])
            except KeyError:
                base_series = None
            splice_series_1 = self.get_data(df, components['new_exports']) - self.get_data(
                df, components['new_imports'])
            if self.country not in FCWVACP:
                u_series = self.get_data(df, components['u_exports']) - self.get_data(df, components['u_imports'])
                splice_series_2 = (splice_series_1 / u_series.shift(1) - 1) * 100
        return base_series, splice_series_1, splice_series_2

    def perform_computation(self, df, ameco_df):
        for variable in NA_VO:
            new_variable = variable + '.1.0.0.0'
            u_variable = re.sub('^.', 'U', variable)
            variable11 = variable + '.1.1.0.0'
            if self.country in FCWVACP:
                try:
                    new_data = self.splicer.ratio_splice(self.get_data(ameco_df, u_variable),
                                                         self.get_data(df, variable), kind='forward')
                except KeyError:
                    logger.error('Failed to calculate {} (national accounts volume).'.format(variable))
                    continue
                new_meta = pd.Series(self.get_meta(new_variable))
                new_series = new_meta.append(new_data)
                self.result = self.result.append(new_series, ignore_index=True)
            else:
                try:
                    series = self.get_data(df, variable)
                    u_series = self.get_data(df, u_variable)
                except KeyError:
                    logger.error('Failed to calculate {} (national accounts volume).'.format(variable))
                    continue
                try:
                    series11 = self.get_data(ameco_df, variable11)
                    series11[2019] = pd.np.nan
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
        omgs, oxgs, obgn, obsn, oigp = 'OMGS.1.0.0.0', 'OXGS.1.0.0.0', 'OBGN.1.0.0.0', 'OBSN.1.0.0.0', 'OIGP.1.0.0.0'
        variables = {omgs: {'ameco': 'OMGS.1.1.0.0', 'goods': 'OMGN', 'services': 'OMSN', 'u_goods': 'UMGN',
                            'u_services': 'UMSN'}}
        variables[oxgs] = {'ameco': 'OXGS.1.1.0.0', 'goods': 'OXGN', 'services': 'OXSN', 'u_goods': 'UXGN',
                                    'u_services': 'UXSN'}
        variables[obgn] = {'exports': 'OXGN.1.1.0.0', 'imports': 'OMGN.1.1.0.0', 'new_exports': 'OXGN',
                                      'u_exports': 'UXGN', 'new_imports': 'OMGN', 'u_imports': 'UMGN'}
        variables[obsn] = {'exports': 'OXSN.1.1.0.0', 'imports': 'OMSN.1.1.0.0', 'new_exports': 'OXSN',
                                      'u_exports': 'UXSN', 'new_imports': 'OMGN', 'u_imports': 'UMGN'}
        variables[oigp] = {'exports': 'OIGT.1.1.0.0', 'imports': 'OIGG.1.1.0.0', 'new_exports': 'OIGG',
                                      'u_exports': 'UIGG', 'new_imports': 'OIGG', 'u_imports': 'UIGG'}

        for variable in variables:
            base_series = None
            try:
                base_series, splice_series_1, splice_series_2 = self._get_data(variable, variables[variable], df,
                                                                               ameco_df)
            except TypeError:
                logger.error('Missing data for variable {} in national accounts volume'.format(variable))
            # if variable == obsn:
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
        export_series = self.get_data(df, goods_exports) + self.get_data(df, services_exports)
        import_series = self.get_data(df, goods_imports) + self.get_data(df, services_imports)
        u_exports = self.get_data(df, u_goods_exports) + self.get_data(df, u_services_exports)
        u_imports = self.get_data(df, u_goods_imports) + self.get_data(df, u_services_imports)
        base_series = self.get_data(ameco_df, ameco_exports) - self.get_data(ameco_df, ameco_imports)
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
        net_series = self.get_data(df, investments_1) - self.get_data(df, investments_2)
        u_net_series = self.get_data(df, u_investments_1) - self.get_data(df, u_investments_2)
        base_series = self.get_data(ameco_df, ameco_1) - self.get_data(ameco_df, ameco_2)
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
        u_series = self.get_data(df, u_new_private_consumption) + self.get_data(
            df, u_new_government_consumption) + self.get_data(df, u_new_use)
        base_series = self.get_data(ameco_df, private_consumption) + self.get_data(
            ameco_df, government_consumption) + self.get_data(ameco_df, use_ameco)
        splice_series_1 = self.get_data(df, new_private_consumption) + self.get_data(
            df, new_government_consumption) + self.get_data(df, new_use)
        splice_series_2 = (splice_series_1 / u_series.shift(1) - 1) * 100
        self._update_result(var, base_series, splice_series_1, splice_series_2)

        # Domestic demand
        variables = {'OUNT.1.0.0.0': ['OUNT.1.1.0.0', 'OCPH', 'OCTG', 'OIGT', 'OIST'],
                     'OUTT.1.0.0.0': ['OUTT.1.1.0.0', 'OCPH', 'OCTG', 'OIGT', 'OIST', 'OXGN', 'OXSN'],
                     'OITT.1.0.0.0': ['OITT.1.0.0.0', 'OIGT', 'OIST']}
        for var, new_vars in variables.items():
            base_series = None
            splice_series_1 = sum([self.get_data(df, v) for v in new_vars[1:]])
            try:
                base_series = self.get_data(df, new_vars[0])
            except KeyError:
                logger.warning('No historical data for {} to level_splice, country {}, using country forecast '
                               'data.'.format(new_vars[0], self.country))
            splice_series_2 = None
            if self.country not in FCWVACP:
                u_new_vars = [re.sub('^.', 'U', v) for v in new_vars[1:]]
                try:
                    sum_u_series = sum(self.get_data(df, v) for v in new_vars[1:])
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

            # TODO: Review this
            new_vars = ['OXGS.1.0.0.0', 'OVGE.1.0.0.0']
            if new_variable in self.result['Variable Code'].values.tolist() + new_vars:
                if new_variable not in new_vars:
                    result_series_index = self.get_index(new_variable)
                    series_orig = self.result.loc[result_series_index]
                    data_orig = pd.to_numeric(series_orig.filter(regex=r'[0-9]{4}'), errors='coerce')
                else:
                    logger.error('Missing data for variable {} in national accounts volume'.format(u1_variable))

                # Rebase to baseperiod
                if u1_variable in df.index.get_level_values('Variable Code'):
                    series_meta = self.get_meta(new_variable)
                    u1_series = self.get_data(df, u1_variable)
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
                series_6_index = self.get_index(variable_6)
                data_6 = self.get_data(self.result, variable_6)
                # series_6 = self.result.loc[result_series_index]
                # data_6 = pd.to_numeric(series_6.filter(regex=r'[0-9]{4}'), errors='coerce')
                xvgd = 'OVGD.1.0.0.0' if self.country in ['MT', 'TR'] else 'UVGD.1.0.0.0'
                series_meta = self.get_meta(variable_c1)
                data_x = self.get_data(df, variable_x).shift(1)
                data_xvgd = self.get_data(df, xvgd).shift(1)
                if variable_c1 not in ['CBGN.1.0.0.0']:
                    try:
                        data_x[1996] = self.get_data(ameco_df, variable_x)[1996]
                    except KeyError:
                        pass
                    try:
                        data_x[1996] = self.get_data(ameco_df, xvgd)[1996]
                    except KeyError:
                        pass
                try:
                    series_data = data_6 * data_x / data_xvgd
                except KeyError:
                    logger.error('Missing data for variable {} in national accounts volume'.format(new_variable))
                    continue
                series = pd.Series(series_meta)
                series = series.append(series_data)
                # if variable_c1 == 'CMGS.1.0.0.0':
                #     import code;code.interact(local=locals())
                self.result = self.result.append(series, ignore_index=True, sort=True)

            else:
                logger.error('Missing data for variable {} in national accounts volume'.format(new_variable))
            r = self.result.copy()
            if new_variable == 'OVGD.1.0.0.0':
                ovgd1 = self.get_data(self.result, 'OVGD.1.0.0.0')
            # if variable_c1 == 'CMGS.1.0.0.0':
            #     import code;code.interact(local=locals())

        # Contribution to percent change in GDP (calculation for additional variables)
        var = 'CMGS.1.0.0.0'
        series_meta = self.get_meta(var)
        series_data = -self.get_data(self.result, var)
        index = self.get_index(var)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result.iloc[index] = series
        var = 'CBGS.1.0.0.0'
        exports = 'CXGS.1.0.0.0'
        imports = 'CMGS.1.0.0.0'
        series_meta = self.get_meta(var)
        series_meta['Variable Code'] = var
        series_data = self.get_data(self.result, exports) + self.get_data(self.result, imports)
        index = self.get_index(var)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        # TODO: If Country in group 'Forecast: Countries with volumes at constant prices' line 202 country calc

        # Per-capita GDP
        # TODO: fix scale, frequency and country everywhere
        # TODO: fix this
        new_variable = 'RVGDP.1.0.0.0'
        ameco_variable = 'RVGDP.1.1.0.0'
        variable_6 = re.sub('.1.0.0.0', '.6.0.0.0', new_variable)
        total_population = 'NPTD.1.0.0.0'
        potential_gdp = 'OVGD.1.0.0.0'
        series_meta = self.get_meta(new_variable)
        series_6_meta = self.get_meta(variable_6)
        ameco_series = self.get_data(ameco_df, ameco_variable)
        splice_series = ovgd1 / self.get_data(df, total_population)
        splicer = Splicer()
        series_data = splicer.ratio_splice(ameco_series, splice_series, kind='forward')
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
            series_data = (self.get_data(df, exports_1[index]) / self.get_data(self.result, exports_2[index]) / (
                    self.get_data(df, imports_1[index]) / self.get_data(self.result, imports_2[index]))) * 100
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
        series_data = self.get_data(self.result, 'OVGD.6.0.0.0')
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        # Convert percent change of trade variables (volume) from national currency to USD
        for variable in T_VO:
            new_variable = variable + '.6.0.30.0'
            variable_6 = variable + '.6.0.0.0'
            series_meta = self.get_meta(new_variable)
            series_data = self.get_data(self.result, variable_6)
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        series_meta = self.get_meta('OVGD.1.0.0.0')
        series = pd.Series(series_meta)
        # TODO: This shouldn't be needed... Check what's going on
        series = series.append(ovgd1)
        self.result = self.result.append(series, ignore_index=True, sort=True)
        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, step=4, country=self.country)
        return self.result, ovgd1
