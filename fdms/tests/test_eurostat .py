
import unittest
from fdms.computation.eurostat import EurostatInput


class TestEurostat(unittest.TestCase):
    '''Tests for "Eurostat" functions'''

    def test_eurostat(self):

        filename = 'fdms/sample_data/Eurostat.xlsx'
        sheet = 'Sheet1'
        calc = EurostatInput()
        result = calc.hicp_quarterly(filename,sheet)

        self.result = result