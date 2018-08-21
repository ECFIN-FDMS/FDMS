import unittest
import pandas as pd

from fdms.helpers.operators import get_series
from fdms.helpers.splicer import Splicer
from fdms.computation.country.annual.national_accounts_volume import NationalAccountsVolume
from fdms.helpers.operators import read_raw_data


class TestNationalAccountsVolume(unittest.TestCase):
    def test_country_with_volumes_at_constant_prices(self):
        pass

    def test_country_not_with_volumes_at_constant_prices(self):
        country = 'BE'
        df, ameco_df = read_raw_data('fdms/sample_data/BE.Forecast.0908.xlsm',
                                     'fdms/sample_data/BE_AMECO.xlsx', 'BE',)
        expected_df = pd.read_excel('fdms/sample_data/BE.raw.0908.xlsx', sheet_name='result-spring2018',
                                    index_col=[2, 3])
        # Variable in National Account variables (Volume)
        # ['OCPH', 'OCTG', 'OIGT', 'OIGCO', 'OIGDW', 'OIGNR', 'OIGEQ', 'OIGOT', 'OIST', 'OITT', 'OUNF', 'OUNT', 'OUTT',
        #     'OVGD', 'OVGE', 'OXGS', 'OMGS', 'OXGN', 'OXSN', 'OMGN', 'OMSN', 'OBGN', 'OBGS', 'OBSN', 'OIGG', 'OIGP']
        variable = 'OCPH'
        new_variable = 'OCPH.1.0.0.0'
        ameco_variable = 'OCPH.1.1.0.0'
        related_variable = 'UCPH'
        expected_result = get_series(expected_df, country, new_variable)
        base_series = get_series(ameco_df, country, ameco_variable)
        splice_series = get_series(df, country, variable) / (
                get_series(df, country, related_variable).shift(1) - 1) * 100
