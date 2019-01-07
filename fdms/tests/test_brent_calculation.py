import pandas as pd
from fdms.computation.brent_calculation import brent_usd, brent_euro, brent_usd_yoy, brent_euro_yoy

filename = 'fdms/sample_data/Commodities.xlsx'

brent_usd_a = brent_usd(filename,'A','Sheet2')

brent_usd_yoy_a = brent_usd_yoy(filename,'Sheet1')

brent_usd_q, columns = brent_usd(filename,'Q','Sheet3')

exchange_rate_us = pd.DataFrame({'2015':[1.11],'2016':[1.11],'2017':[1.07],'2018':[1.07]},index=['XNE.1.0.99.0'])

brent_euro_a,exchange_df = brent_euro(brent_usd_a,exchange_rate_us,'A')

brent_euro_yoy_a = brent_euro_yoy(brent_euro_a)

res = pd.DataFrame(columns=brent_usd_q.columns)
exchange_df.columns = pd.to_datetime(exchange_df.columns,format='%Y',errors='ignore')
result = res.combine_first(exchange_df)
result.reindex_axis(sorted(result.columns),axis=1)
result=result.fillna(method='ffill',axis=1)
result.columns = columns

breakpoint()

result_series = result.loc['Brent(euro).Q']
brent_usd_q_series = brent_usd_q.loc['Brent(euro).Q']

brent_eur_q_series = brent_usd_q_series / result_series
brent_eur_q = brent_eur_q_series.to_frame().T



