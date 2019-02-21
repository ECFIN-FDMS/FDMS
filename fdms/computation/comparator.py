
import pandas as pd
import numpy as np


def compare(calc_name,expected_df, result, filename):

    differences_df = pd.DataFrame()
    wrong_vars = []
    processed_vars = []
    additional_vars = []
    writer = pd.ExcelWriter(filename)

    dates_expect = expected_df.filter(regex='\d{4}').columns.tolist()

    dates_result = result.filter(regex='\d{4}').columns.tolist()

    first_date_expect = dates_expect[0]
    first_date_result = dates_result[0]

    last_date_expect = dates_expect[-1]
    last_date_result = dates_result[-1]


    if first_date_expect < first_date_result:
        for date in range(first_date_expect,first_date_result):
            expected_df = expected_df.drop([date], axis=1)

    if last_date_result < last_date_expect:
        for date in range(last_date_result, last_date_expect):
            result[date+1] = np.nan

    if last_date_result > last_date_expect:
        for date in range(last_date_expect, last_date_result):
            expected_df[date+1] = np.nan

    expected_df = expected_df.reset_index()
    expected_df = expected_df.set_index(['Variable Code'])

    result = result.reset_index()
    result = result.set_index(['Variable Code'])

    for index, row in result.iterrows():
        variable = index
        processed_vars.append(variable)
        calc = result.loc[(variable)].filter(regex='\d{4}')

        calc = calc.astype(np.double)
        calc = calc.round(decimals=3)
        #calc.index = calc.index.astype('int64')

        if variable in expected_df.index.tolist():
            exp = expected_df.loc[(variable)].filter(regex='\d{4}')
            exp.index = exp.index.astype('int64')
            exp = exp.astype(np.double)
            exp = exp.round(decimals=3)
            calc = calc.fillna(value='N')
            exp = exp.fillna(value='N')
            comp = calc == exp

            #differences_df = differences_df.append(comp).astype('int64')
            #verification = differences_df.loc[variable].prod()
            #wrong_vars.append(verification)
            #differences_df['test'] = differences_df.loc[variable].prod()

            #if verification == 0:
                #wrong_vars.append(variable)

            comp = pd.concat([calc, exp], axis=1)
            comp = comp.fillna(value='N')
            comp.columns = ['calc', 'exp']
            comp[(variable)] = comp['calc'] == comp['exp']
            var_comp = comp[comp.columns[2]]
            asd = comp.loc[var_comp == False]

            if not asd.empty:
                #comp.to_excel(writer, variable)
                wrong_vars.append(variable)
            #var_comp = comp
            differences_df = differences_df.append(var_comp).astype('int64')
        else:
            additional_vars.append(variable)

    expected_df = expected_df.reset_index()
    result = result.reset_index()

    expected_vars = set(expected_df['Variable Code'].tolist())
    expected_vars_number = len(set(expected_df.index.tolist()))

    result_vars = set(result['Variable Code'].tolist())
    result_vars_number= len(result_vars)

    missing_vars = expected_vars - result_vars
    missing_vars_df = pd.DataFrame({'Missing Variables': list(missing_vars)})

    missing_vars_number =len(missing_vars)

    wrong_vars = set(wrong_vars)
    wrong_vars_number = len(wrong_vars)

    correct_vars_number = len(result_vars - wrong_vars) if expected_vars_number >= result_vars_number else len(expected_vars - wrong_vars)


    data = {'expected vars': expected_vars_number,
        'correct vars': correct_vars_number,
        'wrong vars': wrong_vars_number,
        'missing vars': missing_vars_number}

    summary = pd.DataFrame(data,index=[calc_name])

    summary.to_excel(writer, 'Summary')
    differences_df.to_excel(writer, 'Differences')

    result.to_excel(writer, 'Results')
    expected_df.to_excel(writer, 'Expected')

    return summary, wrong_vars, missing_vars