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
from config import *
import stock_hist_data as shd
import stock_price_hist as sph
import datetime
import numpy as np
import matplotlib as mpl
import warnings
warnings.filterwarnings('ignore')

sts_date = pd.to_datetime(startdate)
end_date = pd.to_datetime(enddate)
dt = sts_date
asset_hist = {} #Total asset history dict
'''
asset_hist = {XXXX-XX-XX : {date: XXXX-XX-XX, JPN_stock_asset: XX, US_stock_asset: XX} 
            , XXXX-XX-XX : {date: XXXX-XX-XX, JPN_stock_asset: XX, US_stock_asset: XX} 
                    }
'''
hold_asset = {} #Detail stock information history dict
'''
hold_asset = {
    XXXX-XX-XX: 
    {date:XXXX-XX-XX,  stock_info :
             {brandcodeXX: {brand_name:XX, brand_code: XX, Qty: XX, Close_price:XX }}, 
             {brandcodeXX: {brand_name:XX, brand_code: XX, Qty: XX, Close_price:XX }},}
                ,
    XXXX-XX-XX: 
    {date:XXXX-XX-XX, stock_info :
             {brandcodeXX: {brand_name:XX, brand_code: XX, Qty: XX, Close_price:XX }}, 
             {brandcodeXX: {brand_name:XX, brand_code: XX, Qty: XX, Close_price:XX }},}
                    }
'''
time_range = int(str(end_date - sts_date)[:3]) #653
daterange = pd.date_range(pd.to_datetime('2018-10-15'), periods=time_range, freq='d')
pdt = sts_date - timedelta(days=1)
asset_hist[str(pdt)] = {}
asset_hist[str(pdt)]['date'] = str(pdt)
asset_hist[str(pdt)]['JPN_stock_asset'] = 0
asset_hist[str(pdt)]['US_stock_asset'] = 0
hold_asset[str(pdt)] = {}
hold_asset[str(pdt)]['date'] = str(pdt)
hold_asset[str(pdt)]['stock_info'] = {}


def main():
	for cnt, dt in tqdm(enumerate(daterange)):
	   cnt +=1
	   pdt = dt - timedelta(days=1)
	   hold_brand_list = []
	   asset_hist[str(dt)] = {}
	   asset_hist[str(dt)]['date'] = str(dt)
	   asset_hist[str(dt)]['JPN_stock_asset'] = 0
	   asset_hist[str(dt)]['US_stock_asset'] = 0
	   hold_asset[str(dt)] = {}
	   hold_asset[str(dt)]['date'] = str(dt)
	   hold_asset[str(dt)]['stock_info'] = hold_asset[str(pdt)]['stock_info'].copy()
	   if cnt >680:
	       print('id: {}, date: {:%Y-%m-%d}'.format(cnt,dt))
	   
	   #Define trade transaction of the date
	   df = shd.df_trn.query('date == @dt and trade_type=="spot"').copy()
	   df['duplicate'] = df.groupby(['brand', 'trade'])['counter'].transform('cumsum')
	   
	   if len(df)>0: #whether there is any trade
	       phold_brand_list = list(hold_asset[str(pdt)]['stock_info'].keys()) #売買のなかった銘柄
	       
	       rm_list = list(df.brand_code.unique())
	       hold_brand_list = [b for b in phold_brand_list if b not in rm_list]
	       for brd in hold_brand_list:
	           qty =  hold_asset[str(pdt)]['stock_info'][brd]['Qty']#stock quantity
	           brand_code = brd
	           brand_name = hold_asset[str(pdt)]['stock_info'][brd]['brand_name']
	           stock_data = sph.stock_hist.query('Date==@dt & brand_code==@brand_code')
	           #休日か判定
	           if len(stock_data) == 0:
	               #日本株
	               if type(brd) == int:
	                   asset_hist[str(dt)]['JPN_stock_asset'] += qty * hold_asset[str(pdt)]['stock_info'][brd]['Close_price']
	                   hold_asset[str(dt)]['stock_info'][brd] = hold_asset[str(pdt)]['stock_info'][brd].copy()
	                   continue
	               #米国株
	               elif type(brd) == str:
	                   asset_hist[str(dt)]['US_stock_asset'] += qty * hold_asset[str(pdt)]['stock_info'][brd]['Close_price']
	                   hold_asset[str(dt)]['stock_info'][brd] = hold_asset[str(pdt)]['stock_info'][brd].copy()
	                   continue
	           price = stock_data.Close.values[0]
	           brand_info = {brand_code :
	            {'brand_name': brand_name
	           , 'brand_code': brand_code
	           , 'Qty': qty
	           , 'Close_price': price
	           }}
	           
	           #日本株
	           if type(brd) == int:
	               asset_hist[str(dt)]['JPN_stock_asset'] += qty * price
	               hold_asset[str(dt)]['stock_info'].update(brand_info)
	               
	           #米国株
	           elif type(brd) == str:
	               asset_hist[str(dt)]['US_stock_asset'] += qty * price
	               hold_asset[str(dt)]['stock_info'].update(brand_info)

	       for i in range(len(df)):
	           data = df.iloc[i]
	           dup = data.duplicate
	           qty = data.Qty #stock quantity
	           brand_code = data.brand_code
	           buysell_sameday = 1 if len(df.query('brand_code == @brand_code')['trade'].unique()) > 1 else 0
	           brand_name = data.brand
	           stock_data = sph.stock_hist.query('Date==@dt & brand_code==@brand_code')
	           if len(stock_data) == 0:
	               print('The data for {} is not available'.format(brand_name))
	               continue

	           price = stock_data.Close.values[0]
	           brand_info = {brand_code :
	            {'brand_name': brand_name
	           , 'brand_code': brand_code
	           , 'Qty': qty
	           , 'Close_price': price
	           }}
	           
	           if data.date == dt and data.trade == 'buy' and data.price_currency == 'yen':
	               if brand_code in hold_asset[str(pdt)]['stock_info']:
	                   pqty = hold_asset[str(pdt)]['stock_info'][brand_code]['Qty']
	                   asset_hist[str(dt)]['JPN_stock_asset'] += pqty*price
	                   asset_hist[str(dt)]['JPN_stock_asset'] += qty*price
	               else:
	                   asset_hist[str(dt)]['JPN_stock_asset'] += qty*price

	               if brand_code in hold_asset[str(pdt)]['stock_info'] and dup == 1:
	                   qty += hold_asset[str(pdt)]['stock_info'][brand_code]['Qty']
	                   brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': qty
	                        , 'Close_price': price
	                        }}
	                   hold_asset[str(dt)]['stock_info'].update(brand_info)

	               elif dup > 1:
	                   qty += hold_asset[str(dt)]['stock_info'][brand_code]['Qty']
	                   brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': qty
	                        , 'Close_price': price
	                        }}
	                   hold_asset[str(dt)]['stock_info'].update(brand_info)
	               else:
	                   hold_asset[str(dt)]['stock_info'].update(brand_info)


	           elif data.date == dt and data.trade == 'buy' and data.price_currency == 'dollar':
	               if brand_code in hold_asset[str(pdt)]['stock_info']:
	                   pqty = hold_asset[str(pdt)]['stock_info'][brand_code]['Qty']
	                   asset_hist[str(dt)]['US_stock_asset'] += pqty*price
	                   asset_hist[str(dt)]['US_stock_asset'] += qty*price
	               else:
	                   asset_hist[str(dt)]['US_stock_asset'] += qty*price

	               if brand_code in hold_asset[str(pdt)]['stock_info'] and dup == 1:
	                   qty += hold_asset[str(pdt)]['stock_info'][brand_code]['Qty']
	                   brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': qty
	                        , 'Close_price': price
	                        }}
	                   hold_asset[str(dt)]['stock_info'].update(brand_info)

	               elif dup > 1:
	                   qty += hold_asset[str(dt)]['stock_info'][brand_code]['Qty']
	                   brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': qty
	                        , 'Close_price': price
	                        }}
	                   hold_asset[str(dt)]['stock_info'].update(brand_info)
	               else:
	                   hold_asset[str(dt)]['stock_info'].update(brand_info)
	               
	           elif data.date == dt and data.trade == 'sell' and data.price_currency == 'yen':
	               #前日時点で株がある
	               if buysell_sameday ==0 and dup ==1:
	                   pqty = hold_asset[str(pdt)]['stock_info'][brand_code]['Qty']
	                   asset_hist[str(dt)]['JPN_stock_asset'] += pqty*price
	                   asset_hist[str(dt)]['JPN_stock_asset'] -= qty*price
	                   Qty = hold_asset[str(pdt)]['stock_info'][brand_code]['Qty'] - qty
	                   brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': Qty
	                        , 'Close_price': price
	                        }}
	                   if Qty == 0:
	                       hold_asset[str(dt)]['stock_info'].pop(brand_code)
	                   else:
	                       hold_asset[str(dt)]['stock_info'].update(brand_info)

	               else:
	                   asset_hist[str(dt)]['JPN_stock_asset'] -= qty*price
	                   Qty = hold_asset[str(dt)]['stock_info'][brand_code]['Qty'] - qty
	                   brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': Qty
	                        , 'Close_price': price
	                        }}
	                   if Qty == 0:
	                       hold_asset[str(dt)]['stock_info'].pop(brand_code)
	                   else:
	                       hold_asset[str(dt)]['stock_info'].update(brand_info)

	           
	           elif data.date == dt and data.trade == 'sell' and data.price_currency == 'dollar':
	               #前日時点で株がある
	               if buysell_sameday ==0 and dup ==1:
	                   pqty = hold_asset[str(pdt)]['stock_info'][brand_code]['Qty']
	                   asset_hist[str(dt)]['US_stock_asset'] += pqty*price
	                   asset_hist[str(dt)]['US_stock_asset'] -= qty*price
	                   Qty = hold_asset[str(pdt)]['stock_info'][brand_code]['Qty'] - qty
	                   brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': Qty
	                        , 'Close_price': price
	                        }}
	                   if Qty == 0:
	                       hold_asset[str(dt)]['stock_info'].pop(brand_code)
	                   else:
	                       hold_asset[str(dt)]['stock_info'].update(brand_info)

	               else:
	                   asset_hist[str(dt)]['US_stock_asset'] -= qty*price
	                   Qty = hold_asset[str(dt)]['stock_info'][brand_code]['Qty'] - qty
	                   brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': Qty
	                        , 'Close_price': price
	                        }}
	                   if Qty == 0:
	                       hold_asset[str(dt)]['stock_info'].pop(brand_code)
	                   else:
	                       hold_asset[str(dt)]['stock_info'].update(brand_info)
	            
	           else:
	               pass
	                #信用取引等は今回無視する
	   else:
	       hold_brand_list = list(hold_asset[str(pdt)]['stock_info'].keys())
	       for brd in hold_brand_list:
	           qty =  hold_asset[str(pdt)]['stock_info'][brd]['Qty']#stock quantity
	           brand_code = brd
	           brand_name = hold_asset[str(pdt)]['stock_info'][brd]['brand_name']
	           stock_data = sph.stock_hist.query('Date==@dt & brand_code==@brand_code')
	           #休日か判定
	           if len(stock_data) == 0:
	               #日本株
	               if type(brd) == int:
	                   
	                   asset_hist[str(dt)]['JPN_stock_asset'] = asset_hist[str(pdt)]['JPN_stock_asset']
	                   hold_asset[str(dt)]['stock_info'][brd] = hold_asset[str(pdt)]['stock_info'][brd].copy()
	                   
	                   continue
	               #米国株
	               elif type(brd) == str:
	                   asset_hist[str(dt)]['US_stock_asset'] = asset_hist[str(pdt)]['US_stock_asset']
	                   hold_asset[str(dt)]['stock_info'][brd] = hold_asset[str(pdt)]['stock_info'][brd].copy()
	                   continue
	           else:
	               price = stock_data.Close.values[0]
	               
	           
	           #日本株
	           if type(brd) == int:
	               
	               asset_hist[str(dt)]['JPN_stock_asset'] += qty * price
	               brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': qty
	                        , 'Close_price': price
	                        }}
	               hold_asset[str(dt)]['stock_info'].update(brand_info)
	               
	               
	           #米国株
	           elif type(brd) == str:
	               asset_hist[str(dt)]['US_stock_asset'] += qty * price
	               brand_info = {brand_code :
	                        {'brand_name': brand_name
	                        , 'brand_code': brand_code
	                        , 'Qty': qty
	                        , 'Close_price': price
	                        }}
	               hold_asset[str(dt)]['stock_info'].update(brand_info)

	   
	df_asset_history= pd.DataFrame(asset_hist).T.reset_index(drop=True)



	sts = time.time()
	c = CurrencyRates()
	tqdm.pandas()
	df_ex = df_asset_history[['date']]
	df_ex['ex_rate'] = df_ex.date.progress_apply(lambda x:\
	    c.get_rates('USD', pd.to_datetime(x))['JPY'])
	ed=time.time()
	print('FX rate obtained in {:.2f} sec'.format(ed-sts))


	df_asset_history = pd.merge(df_asset_history, df_ex, how='left', on = 'date')
	df_asset_history['US_stock_asset_JPY'] = df_asset_history['US_stock_asset'] * df_asset_history['ex_rate']
	df_asset_history['stock_asset_ttl'] = df_asset_history['JPN_stock_asset']+df_asset_history['US_stock_asset_JPY']

	df_asset_history.to_csv(f'{cdir}/{asset_history}',index=False)

	fig = plt.figure(figsize=(10,5.5))
	ax = fig.add_subplot(1,1,1)
	time_range = len(df_asset_history)
	x = pd.date_range(pd.to_datetime('2018-10-14'), periods=time_range, freq='d')
	x = mdates.date2num(x)
	y=[ list(df_asset_history.JPN_stock_asset.values),
	 list(df_asset_history.US_stock_asset_JPY.values)]
	 
	# Plot
	plt.stackplot(x,y, labels=['JP stock','US stock'])
	yms = mdates.MonthLocator(interval=3) 
	ymFmt = mdates.DateFormatter('%Y-%m')
	ax.xaxis.set_major_locator(yms)
	ax.xaxis.set_major_formatter(ymFmt)
	ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x/10**3))))

	labels = ax.get_xticklabels()

	plt.setp(labels, rotation=45, fontsize=10)
	plt.legend(loc='upper left')
	plt.xlabel('Year-Month')
	plt.ylabel('1,000 JPY')
	plt.title('Stock Asset Price History')
	#plt.show()
	plt.savefig(f'{cdir}/Stock Asset Price History.png')

if __name__ == "__main__":
    main()
    excutiondone = time.time()
    print('Process finished in {:.2f} sec'.format(excutiondone - executionstart))