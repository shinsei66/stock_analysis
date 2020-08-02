import pandas as pd
import yfinance as yf
import os
from tqdm.autonotebook import tqdm
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import locale
from forex_python.converter import CurrencyRates
import seaborn as sns
import matplotlib.dates as mdates
import sys
#sys.path.append('C:\\Users\\skysq\\data_analysis\\stock_analysis')
from config import *
import warnings
warnings.filterwarnings('ignore')



## Import data
df_trn1 = pd.read_csv(os.path.join(cdir,trn1),encoding='SHIFT-JIS')
df_trn2 = pd.read_csv(os.path.join(cdir,trn2),encoding='SHIFT-JIS')


# Change column names
df_trn1.columns = ['date', 'brand', 'brand_code', '市場', 'trade', '期限', 'account', '課税', 'Qty', 'price', 'fee', 'tax', 'settele_date', 'settle_price']
df_trn2.columns = ['date', 'currency', 'brand', 'trade', 'account', 'Qty', 'price', 'settele_date', 'settle_price']

# Align data format
df_trn2['sub_brand'] = df_trn2.brand.apply(lambda x: x.split('/')[0])
df_trn2['brand_code'] = df_trn2.sub_brand.apply(lambda x:x.split()[-1])
df_trn2['brand'] = df_trn2.sub_brand.apply(lambda x:x.split()[:-1])
df_trn2.brand = df_trn2.brand.apply(lambda x:''.join(x))

df_trn1['price_currency'] = 'yen'
df_trn2['price_currency'] = 'dollar'

# Merge JPN and US trade history
df_trn = pd.concat([df_trn1[['date',  'brand', 'brand_code', 'trade', 'account', 'Qty', 'price', 'settele_date', 'settle_price','price_currency']],
df_trn2[['date',  'brand', 'brand_code', 'trade', 'account', 'Qty', 'price', 'settele_date', 'settle_price','price_currency']]
],axis=0)
df_trn.reset_index(inplace=True,drop=True)
print(df_trn.shape)

# Align data expression
df_trn['trade_type'] = df_trn.trade.apply(lambda x:'margin' if x in ['信用新規売', '信用返済売', '信用新規買', '信用返済買'] else 'spot')
for string in ['株式現物買', '株式現物買(募集)', '買付']:
       df_trn.trade = df_trn.trade.replace(string, 'buy')
for string in ['株式現物売',  '売却']:
       df_trn.trade = df_trn.trade.replace(string, 'sell')

df_trn.account = df_trn.account.replace(' NISA ', 'NISA')
df_trn.account = df_trn.account.replace(' 特定 ', '特定')

df_trn.date = df_trn.date.apply(lambda x :x.replace('年', '/').replace('月', '/').replace('日', ''))
df_trn.date = pd.to_datetime(df_trn.date, format='%Y/%m/%d')
df_trn.settele_date = df_trn.settele_date.apply(lambda x:x if len(x)>8 else '20'+x)
df_trn.settele_date = pd.to_datetime(df_trn.settele_date , format='%Y/%m/%d')


brand_list = df_trn[['brand', 'brand_code']].drop_duplicates()

#Change date of the IPO stock for convenience
df_trn.loc[5,'date'] =  pd.to_datetime('2018-12-19')
df_trn.loc[5,'settele_date'] =  pd.to_datetime('2018-12-19')


## Sort trade order for convenience
#['buy', 'sell', '信用新規売', '信用返済売', '信用新規買', '信用返済買']
df_trn['trade_order'] = df_trn.trade.apply(lambda x: 1 if x in ['buy','信用新規売',
'信用新規買'] else 2)
df_trn.sort_values(by=['date', 'trade_order'],inplace=True)

# Set a counter to clarify the multiple trade of the same brand
df_trn['counter'] = 1

# Save cleansed trade history data as a csv file
df_trn.to_csv(f'{cdir}/{trade_hist}', index=False, encoding='SHIFT-JIS')