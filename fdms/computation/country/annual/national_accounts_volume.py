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

    def perform_computation(self, df, ameco_df=None):
        ameco_df = ameco_df if ameco_df is not None else df
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
                    try:
                        series = get_series(df, country, variable)
                        u_series = get_series(df, country, u_variable)
                        series11 = get_series(df, country, variable11)
                    except KeyError:
                        logger.error('Missing data for variable {}'.format(new_variable))
                        continue
                    splice_series = (series / u_series.shift(1) - 1) * 100
                    # RatioSplice(base, level(series)) = base * (1 + 0, 01 * series)
                    new_data = splicer.splice_and_level_forward(series11, splice_series)
                    new_meta = pd.Series({'Variable Code': new_variable, 'Country Ameco': country,
                                          'Frequency': get_frequency(df, country, variable),
                                          'Scale': get_scale(df, country, variable)})
                    new_series = new_meta.append(new_data)
                    result.append(new_series, ignore_index=True)

            # Imports / exports of goods and services
            group_1_vars = ['OMGS.1.0.0.0', 'OXGS.1.0.0.0']
            group_1_ameco = ['OMGS.1.1.0.0', 'OXGS.1.0.0.0']
            group_1_goods = ['OMGN', 'OXGN']
            group_1_services = ['OMSN', 'OXSN']

            # Net imports / exports of goods, services and investments
            group_2_vars = ['OBGN.1.0.0.0', 'OBSN.1.0.0.0', 'OIGP.1.0.0.0']
            group_2_exports = ['OXGN.1.1.0.0', 'OXSN.1.1.0.0', 'OIGT.1.1.0.0']
            group_2_imports = ['OMGN.1.1.0.0', 'OMSN.1.1.0.0', 'OIGG.1.1.0.0']
            group_2_new_exports = ['OXGN', 'OXSN', 'OIGT']
            group_2_new_imports = ['OMGN', 'OMGN', 'OIGG']

            # Net exports goods and services
            var = 'OBGS.1.0.0.0'
            ameco_exports = 'OXGS.1.1.0.0'
            ameco_imports = 'OMGS.1.1.0.0'
            goods_exports = 'OXGN'
            services_exports = 'OXSN'
            goods_imports = 'OMGN'
            services_imports = 'OMSN'

            # Investments
            var = 'OIGNR.1.0.0.0'
            ameco_1 = 'OIGCO.1.1.0.0'
            ameco_2 = 'OIGDW.1.1.0.0'
            investments_1 = 'OIGCO'
            investments_2 = 'OIGDW'

            # Domestic demand
            var = 'OUNF.1.0.0.0'
            private_consumption = 'OCPH.1.1.0.0'
            government_consumption = 'OCTG.1.1.0.0'
            use_ameco = 'OIGT.1.1.0.0'
            new_private_consumption = 'OCPH'
            new_government_consumption = 'OCTG'
            new_use = 'OIGT'

            # Domestic demand
            var = 'OUNT.1.0.0.0'
            ameco_1 = 'OUNT.1.1.0.0'
            private_consumption = 'OCPH'
            government_consumption = 'OCTG'
            use_1 = 'OIGT'
            use_2 = 'OIST'

            # Final demand
            var = 'OUTT.1.0.0.0'
            var_ameco = 'OUTT.1.1.0.0'
            new_private_consumption = 'OCPH'
            new_government_consumption = 'OCTG'
            use_1 = 'OIGT'
            use_2 = 'OIST'
            goods = 'OXGN'
            services = 'OXSN'

            # Gross capital formation
            var = 'OITT.1.0.0.0'
            var_ameco = 'OITT.1.1.0.0'
            use_1 = 'OIGT'
            use_2 = 'OIST'

            if country in FCWVACP:
                pass
