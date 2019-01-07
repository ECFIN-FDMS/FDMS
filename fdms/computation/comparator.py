
import pandas as pd
import numpy as np


def compare(expected_df, expected_vars, result, filename):

    differences_df = pd.DataFrame()
    wrong_vars = []
    processed_vars = []
    additional_vars = []
    writer = pd.ExcelWriter(filename)

    expected_df = expected_df.reset_index()
    expected_df = expected_df.drop(['1990', '1991', '1992'], axis=1)
    expected_df = expected_df.set_index(['Variable'])
    result = result.reset_index()
    result = result.drop([2019], axis=1)
    result = result.set_index(['Variable Code'])

    for index, row in result.iterrows():
        variable = index
        processed_vars.append(variable)
        calc = result.loc[(variable)].filter(regex='\d{4}')
        calc.index = calc.index.astype('int64')
        calc = calc.astype(np.double)
        calc = calc.round(decimals=3)

        if index in expected_vars:
            exp = expected_df.loc[(variable)].filter(regex='\d{4}')
            exp.index = exp.index.astype('int64')
            exp = exp.astype(np.double)
            exp = exp.round(decimals=3)
            comp = pd.concat([calc, exp], axis=1)
            comp = comp.fillna(value='N')
            comp.columns = ['calc', 'exp']
            comp[(variable)] = comp['calc'] == comp['exp']
            var_comp = comp[comp.columns[2]]
            asd = comp.loc[var_comp == False]

            if not asd.empty:
                comp.to_excel(writer, variable)
                wrong_vars.append(variable)
            differences_df = differences_df.append(var_comp).astype('int64')
        else:
            additional_vars.append(variable)

    differences_df.to_excel(writer, 'Differences')
    result.to_excel(writer, 'Results')
    expected_df.to_excel(writer, 'Expected')

    return differences_df, wrong_vars, additional_vars