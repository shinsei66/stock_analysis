import os
import time

# path
cdir = 'C:\\Users\\skysq\\data_analysis\\stock_analysis'

# input file names
trn1 = 'SaveFile_000001_000141.csv' #JPN stocks
trn2 = 'yakujo20200731041039.csv' #US stocks

# output file names
trade_hist = 'trading_history2.csv' #Cleansed trade history
stock_price = 'stock_price.csv' #Gathered stock price data

# parameters
startdate = '2018-10-15' #The minimum date within the trade history data
enddate = '2020-07-28' #The maximum date within the trade history data
asset_history = 'asset_history.csv'
ifexdata = True #In case we have external stock data, set True. we need customize this part by ourselves

executionstart = time.time()

if __name__ == "__main__":
    print('{} \n {} \n {} \n {} \n {}'.format(cdir, trn1, trn2, startdate, enddate))