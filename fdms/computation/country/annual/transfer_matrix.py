import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from fdms.config.variable_groups import TM, NA_VO, TM_TBBO, TM_TBM
from fdms.utils.splicer import Splicer
from fdms.utils.operators import Operators
from fdms.utils.series import get_series, get_scale, get_frequency



class TransferMatrix:
    source_df = pd.DataFrame()

    def perform_computation(self, df, ameco_df):
        result = pd.DataFrame()
        for index, row in df.iterrows():
            country = index[0]
            variable = index[1]
            if variable in TM:
                # Convert all transfer matrix variables to 1.0.0.0 (except National Account (volume)) and splice in
                # country desk forecast
                if variable not in NA_VO:
                    splicer = Splicer()
                    operators = Operators()
                    meta = {'Frequency': get_frequency(df, country, variable),
                            'Scale': get_scale(df, country, variable), 'Country Ameco': country}
                    new_variable = variable + '.1.0.0.0'
                    meta1000 = dict(meta)
                    meta['Variable Code'] = variable
                    meta1000['Variable Code'] = new_variable
                    try:
                        base_series = get_series(ameco_df, country, new_variable)
                        splice_series = get_series(df, country, variable)
                    except KeyError:
                        logger.warning('Missing Ameco data for variable {} (transfer matrix)'.format(new_variable))
                        continue
                    orig_series = splice_series.copy()
                    orig_series.name = None
                    new_meta = pd.Series(meta)
                    orig_series = new_meta.append(orig_series)
                    result = result.append(orig_series, ignore_index=True)
                    if variable in TM_TBBO:
                        new_series = splicer.butt_splice(base_series, splice_series, kind='forward')
                        new_series.name = None
                        new_meta = pd.Series(meta1000)
                        new_series = new_meta.append(new_series)
                        result = result.append(new_series, ignore_index=True)
                    elif variable in TM_TBM:
                        df_to_be_merged = pd.DataFrame([splice_series, base_series])
                        new_series = operators.merge(df_to_be_merged)
                        new_series.name = None
                        new_meta = pd.Series(meta1000)
                        new_series = new_meta.append(new_series)
                        result = result.append(new_series, ignore_index=True)
                    else:
                        new_series = splicer.butt_splice(splicer.ratio_splice(base_series, splice_series, kind='forward'), splice_series, kind='forward')
                        new_series.name = None
                        new_meta = pd.Series(meta1000)
                        new_series = new_meta.append(new_series)
                        result = result.append(new_series, ignore_index=True)

                    # result = result.append(base_series, ignore_index=True)
                    # TODO: find out about parameter "Source" in series?
                    # src_data = operators.iin(splice_series, '', 'Country desk forecast')
                    # src_data = operators.iin(base_series, src_data)
                    # self.source_df = source_df.append()

        column_order = ['Country Ameco', 'Variable Code', 'Frequency', 'Scale', 1993, 1994, 1995, 1996, 1997,
                        1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                        2014, 2015, 2016, 2017, 2018, 2019]
        result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_data = result.copy()
        export_data = export_data.reset_index()
        writer = pd.ExcelWriter('output1.xlsx', engine='xlsxwriter')
        export_data[column_order].to_excel(writer, index_label=[('Country Ameco', 'Variable Code')],
                                           sheet_name='Sheet1', index=False)
        result_vars = result.index.get_level_values('Variable Code').tolist()
        with open('outputvars1.txt', 'w') as f:
            f.write('\n'.join(result_vars))
        return result
