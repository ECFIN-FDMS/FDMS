country_group_names = {
    'FCFTM': 'Forecast: Countries from transfer matrix',
    'FCWVACP': 'Forecast: Countries with volumes at constant prices',
    'EA': 'EA',
    'EU': 'EU',
    'FCFSF': 'Forecast: Countries from small files',
    'FCWEMS1999': 'Forecast: Countries with EA membership since 1999',
    'FCRIF': 'Forecast: Countries reporting in FTEs'
}


FCWVACP = ['EL', 'TR', 'RS', 'US', 'JP']


FCRIF = ['ES', 'FR', 'IT', 'NL']


FCWEMS1999 = ['BE', 'DE', 'IE', 'ES', 'FR', 'IT', 'LU', 'NL', 'AT', 'PT', 'FI']


EA = ['BE', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'IT', 'CY', 'LV', 'LT', 'LU', 'MT', 'NL', 'AT', 'PT', 'SI', 'SK', 'FI']


EU = ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT', 'NL',
      'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'SE', 'FI', 'UK']

FCFSF = ['CA', 'MX', 'KO', 'AU', 'NZ', 'CN', 'HK', 'ID', 'BR', 'IN', 'AR', 'SA', 'ZA']

FCFTM = ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU', 'MT',
         'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'SE', 'FI', 'UK', 'TR', 'MK', 'ME', 'IS', 'RS', 'AL', 'US', 'JP',
         'CH', 'NO', 'RU', 'DAE']


ALL_COUNTRIES = ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE', 'EL', 'ES', 'FR', 'HR', 'IT', 'CY', 'LV', 'LT', 'LU', 'HU',
                 'MT', 'NL', 'AT', 'PL', 'PT', 'RO', 'SI', 'SK', 'SE', 'FI', 'UK', 'TR', 'MK', 'ME', 'IS', 'RS', 'AL',
                 'US', 'JP', 'CA', 'CH', 'NO', 'MX', 'KO', 'AU', 'NZ', 'CN', 'HK', 'RU', 'DL', 'WD', 'ID', 'BL', 'BR',
                 'IN', 'AR', 'SA', 'ZA', 'TW', 'SG']


def get_membership_date(country):
    if country in EA:
        if country in FCWEMS1999:
            return 1999
        elif country == 'EL':
            return 2001
        elif country == 'SI':
            return 2007
        elif country in ['CY', 'MT']:
            return 2008
        elif country == 'SK':
            return 2009
        elif country == 'EE':
            return 2011
        elif country == 'LV':
            return 2014
        elif country == 'LT':
            return 2015
