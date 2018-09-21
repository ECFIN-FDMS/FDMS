import unittest
from fdms.computation.country.eurostat import EurostatInput

class TestEurostat(unittest.TestCase):
    '''Tests for "Eurostat" functions'''

    def test_eurostat(self):

        filename = 'fdms/sample_data/Eurostat.xlsx'
        sheet = 'Sheet2'
        calc = EurostatInput()
        result = calc.hicp_quarterly(filename,sheet)

        self.result = result