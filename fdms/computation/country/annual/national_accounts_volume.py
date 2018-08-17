import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd
import re

from fdms.config.variable_groups import TM, NA_VO, TM_TBBO, TM_TBM
from fdms.config.country_groups import FCWVACP
from fdms.helpers.splicer import Splicer
from fdms.helpers.operators import Operators
from fdms.helpers.operators import get_series, get_scale, get_frequency



class NationalAccountsVolume:
    source_df = pd.DataFrame()

    def perform_computation(self, df, ameco_df):
        result = pd.DataFrame()
        for index, row in df.iterrows():
            country = index[0]
            variable = index[1]
            new_variable = variable + '.1.0.0.0'
            u_variable = re.sub('^.', 'U', variable)
            variable11 = variable + '.1.1.0.0'
            splicer = Splicer()
            operators = Operators()
            if variable in NA_VO:
                if country in FCWVACP:
                    new_data = splicer.ratio_splice(get_series(ameco_df, country, u_variable),
                                                    get_series(df, country, variable), kind='forward')
                    new_meta = pd.Series({'Variable Code': new_variable, 'Country Ameco': country,
                                'Frequency': get_frequency(df, country, variable),
                                'Scale': get_scale(df, country, variable)})
                    new_series = new_meta.append(new_data)
                    result.append(new_series)
                else:
                    new_data = splicer.ratio_splice(get_series(ameco_df, country, u_variable),
                                                    get_series(df, country, variable), kind='forward')
                    new_meta = pd.Series({'Variable Code': new_variable, 'Country Ameco': country,
                                          'Frequency': get_frequency(df, country, variable),
                                          'Scale': get_scale(df, country, variable)})
                    new_series = new_meta.append(new_data)
                    result.append(new_series)