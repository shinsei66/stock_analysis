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
import stock_hist_data
import warnings
warnings.filterwarnings('ignore')

def get_stock(stk):
    if type(stk) is int:
        stk_instance = yf.Ticker(str(stk)+'.T')
    elif type(stk) is str:
        stk_instance = yf.Ticker(stk)

    return stk_instance.history(period="max")

def get_stocks(stks):
    stock_hist = pd.DataFrame()
    print('Downloading stock price ...')
    for stk in tqdm(stks):
        df_tmp = get_stock(stk)
        df_tmp['brand_code'] = stk
        df_tmp.reset_index(inplace=True)
        df_tmp.dropna(inplace=True)
        stock_hist = pd.concat([stock_hist, df_tmp],axis=0,sort=False)
        
    return stock_hist

def main():
    stock_hist = get_stocks(stock_hist_data.brand_list['brand_code'])
    stock_hist.dropna(inplace=True,axis=0,how='all')
    stock_hist.drop('Adj Close',inplace=True, axis=1)
    print(stock_hist.shape)
    if ifexdata:
        df_add = pd.read_csv(f'{cdir}/7352.csv')
        df_add['brand_code'] = 7352
        df_add['Date'] = df_add['Date'].apply(lambda x: pd.to_datetime(x))
        df_add['Dividends'] = 0.0
        df_add['Stock Splits'] = 0.0
        df_add = df_add[['Close', 'Date', 'Dividends', 'High', 'Low', 'Open', 'Stock Splits',
        'Volume', 'brand_code']]
        stock_hist = pd.concat([stock_hist, df_add[['Close', 'Date', 'Dividends', 'High', 'Low', 'Open', 'Stock Splits',
            'Volume', 'brand_code']] ], axis=0,sort=False )
        stock_hist.reset_index(inplace=True, drop=True)
        print(stock_hist.shape)

    stock_hist.to_csv(f'{cdir}/{stock_price}', index=False)
    return stock_hist


stock_hist = main()
#if __name__ == "__main__":
#    main()