import pandas as pd
from fdms.utils.interfaces import read_country_forecast_excel, read_ameco_txt

def brent_usd (filename,frequency,sheet):

    if frequency == 'A':

        com_prices_a = pd.DataFrame()
        crude_petroleum_a = pd.DataFrame()

        # Import Commodity prices - annual
        # filename = 'fdms/sample_data/Commodities.xlsx'
        com_prices_a = pd.read_excel(filename, sheet_name= sheet, header=8)
        com_prices_a = com_prices_a.reset_index()
        com_prices_a = com_prices_a.drop(com_prices_a.columns[[0, 1, 3, 4, 5, 6, 7, 8, 9,10]], axis=1)
        col = com_prices_a.columns
        com_prices_a.columns = ['date','price']
        com_prices_a = com_prices_a.append(pd.Series(col,index=['date','price']),ignore_index=True)
        com_prices_a = com_prices_a.sort_values('date')
        com_prices_a = com_prices_a.T
        com_prices_a.columns = com_prices_a.iloc[0]
        com_prices_a.drop(com_prices_a.index[0], inplace=True)
        com_prices_a.columns = com_prices_a.columns.astype('int64')
        crude_petroleum_a = com_prices_a
        crude_petroleum_a.index=['Crude petroleum,price.A']
        com_prices_a.index=['Brent(usd).A']
        brent_usd_a = com_prices_a

        return brent_usd_a

    elif frequency == 'Q':

        com_prices_q = pd.DataFrame()
        crude_petroleum_q = pd.DataFrame()

        # Import Commodity prices - quarterly
        # filename = 'fdms/sample_data/Commodities.xlsx'
        com_prices_q = pd.read_excel(filename, sheet_name=sheet, header=8)
        com_prices_q = com_prices_q.reset_index()
        com_prices_q = com_prices_q.drop(com_prices_q.columns[[0, 1, 3, 4, 5, 6, 7, 8, 9, 10]], axis=1)
        col = com_prices_q.columns
        com_prices_q.columns = ['date', 'price']
        com_prices_q = com_prices_q.append(pd.Series(col, index=['date', 'price']), ignore_index=True)
        com_prices_q = com_prices_q.sort_values('date')
        com_prices_q = com_prices_q.T
        com_prices_q.columns = com_prices_q.iloc[0]
        com_prices_q.drop(com_prices_q.index[0], inplace=True)
        crude_petroleum_q = com_prices_q
        crude_petroleum_q.index = ['Crude petroleum,price.Q']
        com_prices_q.index = ['Brent(usd).Q']

        com_prices_q.columns = [x.strip().replace('-', 'Q') for x in com_prices_q.columns]
        columns = com_prices_q.columns
        com_prices_q.columns = pd.to_datetime(com_prices_q.columns, errors='ignore')
        #com_prices_q.to_period(freq='Q', axis=1)

        return com_prices_q,columns

def brent_euro (com_prices,exchange_rate_us,frequency):
    if frequency == 'A':
        #exchange_rate_us = merge exchange_rate XR-IR!US|XNE.1.0.99.0[t],AMECO!US|XNE.1.0.99.0[t]

        ameco = read_ameco_txt('fdms/sample_data/AMECO_H.TXT')
        ameco_xne = ameco.loc['US', 'XNE.1.0.99.0']
        ameco_xne = ameco_xne.to_frame()
        ameco_xne = ameco_xne.T.filter(regex='\d{4}').reset_index()
        ameco_xne = ameco_xne.drop(ameco_xne.columns[[0,1]], axis=1)
        ameco_xne.index = ['XNE.1.0.99.0']
        ameco_xne.columns = ameco_xne.columns.astype('int64')
        exchange_rate_us.columns = exchange_rate_us.columns.astype('int64')
        exchange_rate = exchange_rate_us.combine_first(ameco_xne)
        com_prices.columns = com_prices.columns.astype('int64')
        exchange_series = exchange_rate.loc['XNE.1.0.99.0']
        com_prices_series = com_prices.loc['Brent(usd).A']
        com_prices_euro = com_prices_series / exchange_series
        com_prices_euro = com_prices_euro.to_frame().T
        exchange_df = exchange_series.to_frame().T
        com_prices_euro.index = ['Brent(euro).A']
        return com_prices_euro,exchange_df

    elif frequency == 'Q':
        #exchange_rate_us = interpolate(merge exchange_rate XR-IR!US|XNE.1.0.99.0[t],AMECO!US|XNE.1.0.99.0[t])
        com_prices_eur_q = com_prices / exchange_rate_us
        return com_prices_eur_q

def brent_usd_yoy(filename,sheet):

    com_prices_pch = pd.DataFrame()

    # Import Commodity prices pch change
    # filename = 'fdms/sample_data/Commodities.xlsx'
    # sheet_ = 'Sheet1'
    com_prices_pch = pd.read_excel(filename, sheet_name=sheet, header=9)
    com_prices_pch = com_prices_pch.reset_index()
    com_prices_pch = com_prices_pch.drop(com_prices_pch.columns[[0, 2, 3, 4, 5, 6, 7, 8, 9]], axis=1)
    col = com_prices_pch.columns
    com_prices_pch.columns = ['date', 'price']
    com_prices_pch = com_prices_pch.append(pd.Series(col, index=['date', 'price']), ignore_index=True)
    com_prices_pch = com_prices_pch.T
    com_prices_pch.columns = com_prices_pch.iloc[0]
    com_prices_pch.drop(com_prices_pch.index[0], inplace=True)
    #com_prices_pch.columns = com_prices_pch.columns.astype('int64')
    com_prices_pch.index = ['Brent(usd),price.A']

    return com_prices_pch

def brent_euro_yoy(brent_euro):
    brent_euro_yoy = brent_euro.pct_change(axis='columns') * 100
    brent_euro_yoy.index=['Brent(euro),YoY.A']
    return brent_euro_yoy



