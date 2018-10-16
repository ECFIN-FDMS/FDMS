import logging

from fdms.utils.mixins import StepMixin

logging.basicConfig(filename='error.log',
                    format='{%(pathname)s:%(lineno)d} - %(asctime)s %(module)s %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from fdms.utils.splicer import Splicer
from fdms.utils.series import get_series, get_scale, get_frequency, export_to_excel


# STEP 2
class Population(StepMixin):
    def perform_computation(self, df, ameco_df):
        splicer = Splicer()
        # Total labour force (unemployed + employed)
        variable = 'NLTN.1.0.0.0'
        unemployed = 'NUTN.1.0.0.0'
        employed = 'NETN.1.0.0.0'
        country = 'BE'
        base_series = get_series(ameco_df, country, variable)
        splice_series = get_series(df, country, unemployed) + get_series(df, country, employed)
        NLTN1000_meta = self.get_meta(variable)
        NLTN1000_data = splicer.ratio_splice(base_series, splice_series, kind='forward')
        NLTN1000 = pd.Series(NLTN1000_meta)
        NLTN1000 = NLTN1000.append(NLTN1000_data)
        self.result = self.result.append(NLTN1000, ignore_index=True)

        # Self employed (employed - wage and salary earners)
        variable = 'NSTD.1.0.0.0'
        employed = 'NETN.1.0.0.0'
        salary_earners = 'NWTD.1.0.0.0'
        country = 'BE'
        base_series = None
        try:
            base_series = get_series(ameco_df, country, variable)
        except KeyError:
            logger.warning('Missing Ameco data for variable {} (population). Using data '
                           'from country desk forecast'.format(variable))
        splice_series = get_series(df, country, employed) - get_series(df, country, salary_earners)
        NSTD1000_meta = self.get_meta(variable)
        NSTD1000_data = splicer.ratio_splice(base_series, splice_series, kind='forward', variable=variable)
        NSTD1000 = pd.Series(NSTD1000_meta)
        NSTD1000 = NSTD1000.append(NSTD1000_data)
        self.result = self.result.append(NSTD1000, ignore_index=True)

        # Percentage employed (total employed / population of working age (15-64)
        variable = 'NETD.1.0.414.0'
        employed = 'NETD.1.0.0.0'
        working_age = 'NPAN1.1.0.0.0'
        country = 'BE'
        NETD104140_meta = self.get_meta(variable)
        NETD104140_data = get_series(df, country, employed) - get_series(df, country, working_age) * 100
        NETD104140 = pd.Series(NETD104140_meta)
        NETD104140 = NETD104140.append(NETD104140_data)
        self.result = self.result.append(NETD104140, ignore_index=True)

        # Civilian employment
        variable = 'NECN.1.0.0.0'
        employed = 'NETN.1.0.0.0'
        NECN1000_meta = self.get_meta(variable)
        NECN1000_data = splicer.ratio_splice(get_series(ameco_df, country, variable), get_series(df, country, employed),
                                             kind='forward')#, bp=True)
        NECN1000 = pd.Series(NECN1000_meta)
        NECN1000 = NECN1000.append(NECN1000_data)
        self.result = self.result.append(NECN1000, ignore_index=True)

        # Total annual hours worked
        variable = 'NLHT.1.0.0.0'
        average_hours = 'NLHA.1.0.0.0'
        employed = 'NETD.1.0.0.0'
        total_hours_data = get_series(df, country, employed) * get_series(df, country, average_hours)
        NLHT1000_meta = self.get_meta(variable)
        NLHT1000_data = splicer.ratio_splice(get_series(ameco_df, country, variable), total_hours_data, kind='forward')
        NLHT1000 = pd.Series(NLHT1000_meta)
        NLHT1000 = NLHT1000.append(NLHT1000_data)
        self.result = self.result.append(NLHT1000, ignore_index=True)

        # Total annual hours worked; total economy. for internal use only
        variable = 'NLHT9.1.0.0.0'
        average_hours = 'NLHA.1.0.0.0'
        employed = 'NETD.1.0.0.0'
        total_hours_data = get_series(df, country, employed) * get_series(df, country, average_hours)
        NLHT91000_meta = self.get_meta(variable)
        NLHT91000_data = splicer.ratio_splice(get_series(ameco_df, country, variable), total_hours_data, kind='forward')
        NLHT91000 = pd.Series(NLHT91000_meta)
        NLHT91000 = NLHT91000.append(NLHT91000_data)
        self.result = self.result.append(NLHT91000, ignore_index=True)

        # Civilian labour force
        variable = 'NLCN.1.0.0.0'
        civilian_employment = 'NECN.1.0.0.0'
        unemployed = 'NUTN.1.0.0.0'
        NLCN1000_meta = self.get_meta(variable)
        try:
            base_series = get_series(ameco_df, country, variable)
        except KeyError:
            logger.warning('Missing Ameco data for variable {} (population). Using data '
                           'from country desk forecast'.format(variable))
        NLCN1000_data = splicer.ratio_splice(base_series, NECN1000_data + get_series(df, country, unemployed),
                                             kind='forward', variable=variable)#, bp=True)
        NLCN1000 = pd.Series(NLCN1000_meta)
        NLCN1000 = NLCN1000.append(NLCN1000_data)
        self.result = self.result.append(NLCN1000, ignore_index=True)

        self.result.set_index(['Country Ameco', 'Variable Code'], drop=True, inplace=True)
        self.apply_scale()
        export_to_excel(self.result, 'output/outputvars2.txt', 'output/output2.xlsx',)
        return self.result
