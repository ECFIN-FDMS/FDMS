import pandas as pd
import re

from fdms.config.variable_groups import NA_IS_VA
from fdms.utils.series import get_series, get_series_noindex


class NationalAccountsValue:
    result = pd.DataFrame()
    country = 'BE'
    frequency = 'Annual'

    def perform_computation(self, df, ovgd1):
        variables = ['UVGN.1.0.0.0', 'UTVNBP.1.0.0.0', 'UVGE.1.0.0.0', 'UWSC.1.0.0.0']
        component_1 = ['UVGD.1.0.0.0', 'UTVTBP.1.0.0.0', 'UVGD.1.0.0.0', 'UWCD.1.0.0.0']
        component_2 = ['UBRA.1.0.0.0', 'UYVTBP.1.0.0.0', 'UTVNBP.1.0.0.0', 'UWWD']
        for index, variable in enumerate(variables):
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                           'Scale': 'units'}
            if index == 0:
                series_data = get_series(df, self.country, component_1[index]) + get_series(
                    df, self.country, component_2[index])
            elif index == 1:
                series_data = get_series(df, self.country, component_1[index]) - get_series(
                    df, self.country, component_2[index])
                utvnbp = series_data.copy()
            elif index == 2:
                series_data = get_series(df, self.country, component_1[index]) + utvnbp
            else:
                series_data = get_series(df, self.country, component_1[index]) - get_series(
                    df, self.country, component_2[index])
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'UOGD.1.0.0.0'
        components = ['UVGD.1.0.0.0', 'UYVG.1.0.0.0', 'UYEU.1.0.0.0', 'UWCD.1.0.0.0', 'UTVG.1.0.0.0', 'UTEU.1.0.0.0']
        series = [get_series(df, self.country, var) for var in components[:3]]
        series.extend([-get_series(df, self.country, var) for var in components[3:]])
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'units'}
        series_data = sum(series)
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        variable = 'UWCDA.1.0.0.0'
        total_employment = 'NETD.1.0.0.0'
        compensation = 'UWCD.1.0.0.0'
        real_compensation = 'NWTD.1.0.0.0'
        series_meta = {'Country Ameco': self.country, 'Variable Code': variable, 'Frequency': 'Annual',
                       'Scale': 'units'}
        series_data = (get_series(df, self.country, total_employment) * get_series(df, self.country, compensation) /
                       get_series(df, self.country, real_compensation))
        series = pd.Series(series_meta)
        series = series.append(series_data)
        self.result = self.result.append(series, ignore_index=True, sort=True)

        for variable in NA_IS_VA:
            variable_1 = variable + '.1.0.0.0'
            variable_cc = re.sub('^U', 'CC', variable_1)
            series_meta = {'Country Ameco': self.country, 'Variable Code': variable_cc, 'Frequency': 'Annual',
                           'Scale': 'units'}
            try:
                pch = get_series(df, self.country, variable_1) / ovgd1
            except KeyError:
                pch = get_series_noindex(self.result, self.country, variable_1) / ovgd1
            pch = pch.pct_change()
            try:
                series_data = get_series(df, self.country, variable_1) / get_series(
                    df, self.country, 'UVGD.1.0.0.0') * pch
            except KeyError:
                series_data = get_series_noindex(self.result, self.country, variable_1) / get_series(
                    df, self.country, 'UVGD.1.0.0.0') * pch
            series = pd.Series(series_meta)
            series = series.append(series_data)
            self.result = self.result.append(series, ignore_index=True, sort=True)

        column_order = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1993, 1994, 1995, 1996, 1997,
                        1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                        2014, 2015, 2016, 2017, 2018, 2019]
        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_data = self.result.copy()
        export_data = export_data.reset_index()
        writer = pd.ExcelWriter('output/output5.xlsx', engine='xlsxwriter')
        export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                           sheet_name='Sheet1', index=False)
        result_vars = self.result.index.get_level_values('Variable Code').tolist()
        with open('output/outputvars5.txt', 'w') as f:
            f.write('\n'.join(result_vars))
        return self.result
