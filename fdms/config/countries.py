import pandas as pd


COUNTRIES = pd.Series({
    'BE': 'BEL', 'BG': 'BGR', 'CZ': 'CZE', 'DK': 'DNK', 'DE': 'DEU', 'EE': 'EST', 'IE': 'IRL', 'EL': 'GRC', 'ES': 'ESP',
    'FR': 'FRA', 'HR': 'HRV', 'IT': 'ITA', 'CY': 'CYP', 'LV': 'LVA', 'LT': 'LTU', 'LU': 'LUX', 'HU': 'HUN', 'MT': 'MLT',
    'NL': 'NLD', 'AT': 'AUT', 'PL': 'POL', 'PT': 'PRT', 'RO': 'ROM', 'SI': 'SVN', 'SK': 'SVK', 'SE': 'SWE', 'FI': 'FIN',
    'UK': 'GBR', 'TR': 'TUR', 'MK': 'MKD', 'ME': 'MNE', 'IS': 'ISL', 'RS': 'SRB', 'AL': 'ALB', 'US': 'USA', 'JP': 'JPN',
    'CA': 'CAN', 'CH': 'CHE', 'NO': 'NOR', 'MX': 'MEX', 'KO': 'KOR', 'AU': 'AUS', 'NZ': 'NZL', 'CN': 'CHN', 'HK': 'HKG',
    'RU': 'RUS', 'DL': 'DEL', 'WD': 'D_W', 'ID': 'IDN', 'BL': 'BLU', 'BR': 'BRA', 'IN': 'IND', 'AR': 'ARG', 'SA': 'SAU',
    'ZA': 'ZAF', 'AC05': 'AC05', 'AC10': 'AC10',
    'Acceding and Candidate Countries ': 'Acceding and Candidate Countries',
    'Acceding Countries': 'Acceding Countries', 'Advanced economies': 'Advanced economies',
    'Advanced economies, non-EU, non-ACC': 'Advanced economies, non-EU, non-ACC', 'All Countries': 'All Countries',
    'All countries and groups': 'All countries and groups', 'All country groups': 'All country groups',
    'AMT': 'AMT', 'Asia': 'Asia', 'BAL3': 'BAL3', 'BRI': 'BRI', 'CA12': 'CA12',
    'Candidate Countries': 'Candidate Countries', 'CC12': 'CC12', 'CIS': 'CIS', 'CU15': 'CU15', 'CU65': 'CU65',
    'DA12': 'DA12', 'DAE': 'DAE', 'DU15': 'DU15', 'DU25': 'DU25', 'DU27': 'DU27', 'DU65': 'DU65',
    'Dynamic Asian Economies': 'Dynamic Asian Economies', 'EA': 'EA', 'Euro area, adjusted': 'Euro area, adjusted',
    'EA country groups': 'EA country groups', 'EA12': 'EA12', 'EA13': 'EA13', 'EA15': 'EA15', 'EA16': 'EA16',
    'EA17': 'EA17', 'EA18': 'EA18', 'EFTA': 'EFTA',
    'Emerging and developing economies': 'Emerging and developing economies', 'EU': 'EU',
    'EU, adjusted': 'EU, adjusted', 'EU03': 'EU03', 'EU04': 'EU04', 'EU07 ': 'EU07', 'EU08': 'EU08', 'EU11': 'EU11',
    'EU11DE': 'EU11DE', 'EU12 ': 'EU12', 'EU12DC': 'EU12DC', 'EU12DE': 'EU12DE', 'EU15 ': 'EU15', 'EU15DE': 'EU15DE',
    'EU16': 'EU16', 'EU17': 'EU17', 'EU20': 'EU20', 'EU25': 'EU25', 'EU27': 'EU27', 'EU28': 'EU28',
    'FA11': 'FA11', 'FA12': 'FA12', 'FA14': 'FA14', 'FA15': 'FA15', 'FA16': 'FA16', 'FA17': 'FA17',
    'Forecast: Countries from small files': 'Forecast: Countries from small files',
    'Forecast: Countries from transfer matrix': 'Forecast: Countries from transfer matrix',
    'Forecast: Countries from transfer matrix and small files': ('Forecast: Countries from transfer matrix and small '
                                                                 'files'),
    'Forecast: Countries with EA membership since 1999': 'Forecast: Countries with EA membership since 1999',
    'Forecast: Countries with volumes at constant prices': 'Forecast: Countries with volumes at constant prices',
    'Forecast: Countries with volumes at previous year prices': ('Forecast: Countries with volumes at previous year '
                                                                 'prices'),
    'Forecast: Country groups for aggregation': 'Forecast: Country groups for aggregation',
    'FU12': 'FU12', 'FU14': 'FU14', 'FU15': 'FU15', 'FU23': 'FU23', 'FU26': 'FU26', 'FU27': 'FU27',
    'FU35': 'FU35', 'G20': 'G20', 'Latin America': 'Latin America',
    'MENA (Middle East and Northern Africa)': 'MENA (Middle East and Northern Africa)',
    'MENA and Sub-Sahara Africa': 'MENA and Sub-Sahara Africa', 'Non-EA EU countries': 'Non-EA EU countries',
    'OECD': 'OECD', 'Other Asia': 'Other Asia', 'Other CIS': 'Other CIS',
    'Other Emerging Markets': 'Other Emerging Markets', 'Other Latin America': 'Other Latin America',
    'Other OECD Countries': 'Other OECD Countries',
    'Output gap: Country groups to be aggregated': 'Output gap: Country groups to be aggregated',
    'Potential Candidates': 'Potential Candidates', 'Small Non EU': 'Small Non EU',
    'Sub-Saharan Africa': 'Sub-Saharan Africa',
    'TCE: Additional aggregation groups': 'TCE: Additional aggregation groups',
    'TCE: additional country groups to be aggregated': 'TCE: additional country groups to be aggregated',
    'TCE: Countries and Groups': 'TCE: Countries and Groups',
    'TCE: Countries from Matrices': 'TCE: Countries from Matrices', 'TCE: Country groups': 'TCE: Country groups',
    'TCE: Other Advanced Economies': 'TCE: Other Advanced Economies', 'TCE: Reported Total': 'TCE: Reported Total',
    'TCE: Rest of Asia': 'TCE: Rest of Asia',
    'World': 'World', 'World Aggregate: Country Groups': 'World Aggregate: Country Groups',
    'World excluding EU': 'World excluding EU', 'World excluding euro area': 'World excluding euro area',
    'Forecast: Countries reporting in FTEs': 'Forecast: Countries reporting in FTEs', 'EA19': 'EA19', 'IL': 'ISR',
    'TW': 'TWN', 'SG': 'SGP', 'AdvancedEconomiesExclEU': 'AdvancedEconomiesExclEU',
    'EmergingExclChina': 'EmergingExclChina', 'AsiaExclChina': 'AsiaExclChina', 'EA19exIE': 'EA19exIE',
    'EU28exUK': 'EU28exUK'
})
