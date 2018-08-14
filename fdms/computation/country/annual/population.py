import logging

logging.basicConfig(filename='error.log', format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from fdms.config.variable_groups import TM, NA_VO, TM_TBBO, TM_TBM
from fdms.helpers.splicer import Splicer
from fdms.helpers.operators import Operators
from fdms.helpers.operators import get_series, get_scale, get_frequency



class Population:
    source_df = pd.DataFrame()

    def perform_computation(self, df, ameco_df):
        result = pd.DataFrame()
        splicer = Splicer()
        # Total labour force (unemployed + employed)
        variable = 'NLTN.1.0.0.0'
        unemployed = 'NUTN.1.0.0.0'
        employed = 'NETN.1.0.0.0'
        country = 'BE'
        base_series = get_series(ameco_df, country, variable)
        splice_series = get_series(df, country, unemployed) + get_series(df, country, employed)
        NLTN1000_meta = {'Country Ameco': country, 'Variable Code': variable,
                         'Frequency': get_frequency(df, country, employed), 'Scale': get_scale(df, country, employed)}
        NLTN1000_data = splicer.ratio_splice(base_series, splice_series, kind='forward')
        NLTN1000 = pd.Series(NLTN1000_meta)
        NLTN1000 = NLTN1000.append(NLTN1000_data)
        result.append(NLTN1000, ignore_index=True)

        # Self employed (employed - wage and salary earners)
        variable = 'NSTD.1.0.0.0'
        employed = 'NETN.1.0.0.0'
        salary_earners = 'NWTD.1.0.0.0'
        country = 'BE'
        base_series = get_series(ameco_df, country, variable)
        splice_series = get_series(df, country, employed) - get_series(df, country, salary_earners)
        NSTD1000_meta = {'Country Ameco': country, 'Variable Code': variable,
                         'Frequency': get_frequency(df, country, employed), 'Scale': get_scale(df, country, employed)}
        NSTD1000_data = splicer.ratio_splice(base_series, splice_series, kind='forward')
        NSTD1000 = pd.Series(NSTD1000_meta)
        NSTD1000 = NSTD1000.append(NSTD1000_data)
        result.append(NSTD1000, ignore_index=True)

        # Percentage employed (total employed / population of working age (15-64)
        variable = 'NETD.1.0.414.0'
        employed = 'NETD.1.0.0.0'
        working_age = 'NPAN.1.1.0.0'
        country = 'BE'
        NETD104140_meta = {'Country Ameco': country, 'Variable Code': variable,
                         'Frequency': get_frequency(df, country, employed), 'Scale': get_scale(df, country, employed)}
        NETD104140_data = get_series(df, country, employed) - get_series(df, country, working_age) * 100
        NETD104140 = pd.Series(NETD104140_meta)
        NETD104140 = NETD104140.append(NETD104140_data)
        result.append(NETD104140, ignore_index=True)

