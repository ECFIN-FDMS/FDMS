import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from fdms.config.variable_groups import TM, NA_VO, TM_TBBO, TM_TBM
from fdms.helpers.splicer import Splicer
from fdms.helpers.operators import Operators
from fdms.helpers.operators import get_series, get_scale, get_frequency



class TransferMatrix:
    def perform_computation(self, df, ameco_df):
        result = pd.DataFrame()
        for index, row in df.iterrows():
            country = index[0]
            variable = index[1]
            if variable in TM:
                if variable not in NA_VO:
                    new_variable = variable + '.1.0.0.0'
                    splicer = Splicer()
                    operators = Operators()
                    try:
                        base_series = get_series(ameco_df, country, new_variable)
                        splice_series = get_series(df, country, variable)
                    except KeyError:
                        logger.warning('Missing data for variable {}'.format(new_variable))
                        continue
                    if variable in TM_TBBO:
                        new_series = splicer.butt_splice(base_series, splice_series, kind='forward')
                        new_series.name = None
                        new_series.loc['Frequency'] = get_frequency(df, country, variable)
                        new_series.loc['Scale'] = get_scale(df, country, variable)
                        new_series.loc['Country Ameco'] = country
                        new_series.loc['Variable Code'] = new_variable
                        result = result.append(new_series, ignore_index=True)
                    elif variable in TM_TBM:
                        df_to_be_merged = pd.DataFrame([splice_series, base_series])
                        new_series = operators.merge(df_to_be_merged)
                        new_series.name = None
                        new_series.loc['Frequency'] = get_frequency(df, country, variable)
                        new_series.loc['Scale'] = get_scale(df, country, variable)
                        new_series.loc['Country Ameco'] = country
                        new_series.loc['Variable Code'] = new_variable
                        result = result.append(new_series, ignore_index=True)
                    else:
                        rsplice = splicer.ratio_splice(base_series, splice_series, kind='forward')
                        new_series = splicer.butt_splice(rsplice, splice_series, kind='forward')
                        new_series.name = None
                        new_series.loc['Frequency'] = get_frequency(df, country, variable)
                        new_series.loc['Scale'] = get_scale(df, country, variable)
                        new_series.loc['Country Ameco'] = country
                        new_series.loc['Variable Code'] = new_variable
                        result = result.append(new_series, ignore_index=True)

        result = result.set_index(['Country Ameco', 'Variable Code'])
        result = result.reset_index()
        writer = pd.ExcelWriter('output1.xlsx', engine='xlsxwriter')
        result.to_excel(writer, index_label=[('Country Ameco', 'Variable Code')], sheet_name='Sheet1', index=False)
