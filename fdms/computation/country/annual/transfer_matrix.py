import logging

logging.basicConfig(filename='error.log',
                    format='{%(pathname)s:%(lineno)d} - %(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from fdms.config.variable_groups import TM, NA_VO, TM_TBBO, TM_TBM
from fdms.utils.splicer import Splicer
from fdms.utils.operators import Operators
from fdms.utils.series import get_series, get_scale, get_frequency, export_to_excel



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
                    splice_series = get_series(df, country, variable)
                    try:
                        base_series = get_series(ameco_df, country, new_variable)
                    except KeyError:
                        logger.warning('Missing Ameco data for variable {} (transfer matrix)'.format(new_variable))
                    orig_series = splice_series.copy()
                    orig_series.name = None
                    new_meta = pd.Series(meta)
                    orig_series = new_meta.append(orig_series)
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
                        new_series = splicer.butt_splice(splicer.ratio_splice(
                            base_series, splice_series, kind='forward'), splice_series, kind='forward')
                        new_series.name = None
                        new_meta = pd.Series(meta1000)
                        new_series = new_meta.append(new_series)
                        result = result.append(new_series, ignore_index=True)
                    result = result.append(orig_series, ignore_index=True)

        result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        export_to_excel(result, 'output/outputvars1.txt', 'output/output1.xlsx')
        return result
