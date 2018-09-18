import datetime
import re

from fdms.config.variable_groups import TM
from fdms.utils.custom_groups import EXPECTED_VARS_1
from fdms.utils.interfaces import read_country_forecast_excel, FORECAST


COUNTRY_CALCULATION_TXT = 'fdms/utils/country_calculation.txt'


class Helpers:
    indicator_general_regex = re.compile('(.Country.*)[t]')
    historical_regex = re.compile('((AMECO|Historical)!.Country.*)[t]')
    eurostat_regex = re.compile('(input!.Country.*)[t]')
    country_regex = re.compile('[^lOt].(.Country.*)[t]')

    def check_individual_vars(self):
        pass

    def get_usages(self, indicator):
        regex = re.compile('.*{}.*'.format(indicator))
        with open(COUNTRY_CALCULATION_TXT, 'r') as f:
            calculations = regex.findall(f.read())
        calculations = list(set([calc.strip() for calc in calculations]))
        return calculations

    def get_calculations_for(self, indicator):
        regex = re.compile('.*{}.*'.format(indicator))
        calculations = self.get_usages(indicator)
        result = []
        for line in calculations:
            if not re.match('.*=', line):
                continue
            new_var, calculation = line.split('=')
            if regex.match(new_var):
                result.append(line)
        return result

    def get_calculations_using(self, indicator):
        regex = re.compile('.*{}.*'.format(indicator))
        calculations = self.get_usages(indicator)
        result = []
        for line in calculations:
            if not re.match('.*=', line):
                continue
            new_var, calculation = line.split('=')
            if regex.match(calculation):
                result.append(line)
        return result

    def get_variables_needed_for(self, indicator):
        calculations = self.get_calculations_for(indicator)

    def read_country_calculations(self):
        with open('fdms/utils/country_calculation.txt') as f:
            return [x.strip() for x in f.read().splitlines()]

    def read_test_calculations(self):
        with open('fdms/utils/test1.txt') as f:
            return [x.strip() for x in f.read().splitlines()]

    def get_input_vars_from_excel(self, filename=FORECAST):
        df = read_country_forecast_excel(filename)
        return df.index.get_level_values('Variable').tolist()

    def get_output_vars_from_step(self, step):
        filename = 'outputvars' + str(step) + '.txt'
        with open(filename) as f:
            return f.read().splitlines()


def write_report(self, indicator_list=[]):
    now = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y-%H:%M')
    h = Helpers()
    with open('report_{}.txt'.format(now), 'w') as f:
        for var in indicator_list:
            f.write('----------          {}          ----------\n'.format(var))
            f.write('\n'.join(h.get_calculations_for(var)))
            f.write('\n')
            f.write('-----     USAGES     -----\n')
            f.write('\n'.join(h.get_calculations_using(var)))
            f.write('\n\n\n')
