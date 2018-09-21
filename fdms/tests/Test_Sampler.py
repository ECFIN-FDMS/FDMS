import pandas as pd
import unittest
from fdms.computation.country.Eurostat import EurostatInput
from fdms.config.variable_groups import HICP
#import pdb; pdb.set_trace()

class TestSampler(unittest.TestCase):
    '''Tests for "Sampler" functions'''

    def test_sampler(self):

        filename = 'C:\Files\ALLEUSTATM.xlsx'
        sheet = 'Sheet2'
        tag = '1.0.0.0'

        dataframe = pd.read_excel(filename, sheet_name=sheet, header=0)
        dataframe.loc[dataframe['Variable'].isin(HICP)]
        dataframe['Code'] = dataframe['Series'].str.split('.', 1).str[0]

        dataframe['Series'] = dataframe['Code'] + '.' + tag + '.' + dataframe['Variable'] + '.'
        dataframe['Variable'] = dataframe['Variable'] + '.' + tag
        dataframe.drop(columns=['Code'], inplace=True)

        calc = EurostatInput()

        monthly = calc.dataframe_sampler(dataframe,'M')
        quarterly = calc.dataframe_sampler(dataframe,'Q')
        annually = calc.dataframe_sampler(dataframe,'A')

        self.result = quarterly




