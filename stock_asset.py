import warnings
import glob
import matplotlib as mpl
import numpy as np
import datetime
import stock_price_hist as sph
import stock_hist_data as shd
from config import *
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
import time
sys.path.append('C:\\Users\\skysq\\data_analysis\\stock_analysis')
warnings.filterwarnings('ignore')

sts_date = pd.to_datetime(startdate)
end_date = pd.to_datetime(enddate)
dt = sts_date


def read_csvlist(list):
    df_tmp = pd.DataFrame()
    df_list = []
    for f in tqdm(list):
        df_tmp = pd.read_csv(f'{f}', encoding='SHIFT-JIS')
        if '預金・現金・暗号資産（円）' in df_tmp.columns.tolist():
            df_tmp.rename(
                columns={
                    '預金・現金・暗号資産（円）': '預金・現金・仮想通貨（円）'},
                inplace=True)
        df_list.append(df_tmp)
    df = pd.concat(df_list, sort=False, axis=0)
    print(df.shape)
    df.reset_index(drop=True, inplace=True)
    return df


def main():
    df_asset_history = pd.read_csv(f'{cdir}/{asset_history}.csv')
    file_list = glob.glob(f'{cdir}/history/*.csv')
    df = read_csvlist(file_list)

    df['日付'] = df['日付'].apply(lambda x: pd.to_datetime(x))
    df_asset_history['date'] = pd.to_datetime(df_asset_history['date'])
    df = pd.merge(df,
                  df_asset_history[['date',
                                    'stock_asset_ttl']],
                  how='left',
                  left_on='日付',
                  right_on='date')
    df.fillna(0, inplace=True)

    df['株式(現物)（円）'] = df['株式(現物)（円）'].copy() + df['stock_asset_ttl'].copy()

    df.columns = [
        'date',
        'total',
        'cash',
        'point',
        'stock',
        'pension',
        'trust',
        'margin',
        'bond',
        'date1',
        'stock_asset_ttl']
    df = df[['date', 'total', 'cash', 'point',
             'stock', 'pension', 'trust', 'bond', 'margin']]
    df['ym'] = partition
    df.to_csv(f'{cdir}/asset_history_{partition}.csv', index=False)
    df_stack = df.set_index(['date', 'ym']).stack(dropna=False).reset_index()
    df_stack.columns = ['date', 'ym', 'dimension', 'value']
    df_stack.to_csv(f'{cdir}/asset_history_stack_{partition}.csv', index=False)

    # # Plot
    # fig = plt.figure(figsize=(10,5.5))
    # ax = fig.add_subplot(1,1,1)
    # time_range = len(df_asset_history)
    # x = pd.date_range(pd.to_datetime('2018-10-14'), periods=time_range, freq='d')
    # x = mdates.date2num(x)
    # y=[ list(df_asset_history.JPN_stock_asset.values),
    #  list(df_asset_history.US_stock_asset_JPY.values)]

    # plt.stackplot(x,y, labels=['JP stock','US stock'])
    # yms = mdates.MonthLocator(interval=3)
    # ymFmt = mdates.DateFormatter('%Y-%m')
    # ax.xaxis.set_major_locator(yms)
    # ax.xaxis.set_major_formatter(ymFmt)
    # ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x/10**3))))

    # labels = ax.get_xticklabels()

    # plt.setp(labels, rotation=45, fontsize=10)
    # plt.legend(loc='upper left')
    # plt.xlabel('Year-Month')
    # plt.ylabel('1,000 JPY')
    # plt.title('Stock Asset Price History')
    # #plt.show()
    # plt.savefig(f'{cdir}/Stock Asset Price History_{partition}.png')

    # 資産内訳の可視化
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)
    time_range = len(df)
    x = pd.date_range(
        pd.to_datetime('2014-08-24'),
        periods=time_range,
        freq='d')
    x = mdates.date2num(x)
    y = [list(df['cash'].values),
         list(df['stock'].values),
         list(df['pension'].values),
         list(df['trust'].values),
         list(df['bond'].values),
         list(df['margin'].values),
         list(df['point'].values),
         ]

    # Plot
    plt.stackplot(
        x,
        y,
        labels=[
            'Cash',
            'Stock',
            'Pension',
            'ETF',
            'Bond',
            'Margin'
            'Point'])
    yms = mdates.MonthLocator(interval=3)
    ymFmt = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_locator(yms)
    ax.xaxis.set_major_formatter(ymFmt)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(
        lambda x, loc: "{:,}".format(int(x / 10**3))))

    labels = ax.get_xticklabels()

    plt.setp(labels, rotation=45, fontsize=10)
    plt.legend(loc='upper left')
    plt.xlabel('Year-Month')
    plt.ylabel('1,000 JPY')
    plt.title('Asset History')
    plt.savefig(f'{cdir}/Asset_History_{partition}.png')


if __name__ == "__main__":
    main()
    excutiondone = time.time()
    print(
        'Process finished in {:.2f} sec'.format(
            excutiondone -
            executionstart))
