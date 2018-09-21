
import unittest
from fdms.computation.country.Eurostat import EurostatInput

#import pdb; pdb.set_trace()

class TestEurostat(unittest.TestCase):
    '''Tests for "Eurostat" functions'''

    def test_eurostat(self):

        filename = 'C:\Files\ALLEUSTATM.xlsx'
        sheet = 'Sheet2'
        calc = EurostatInput()
        result = calc.hicp_quarterly(filename,sheet)

        self.result = result