import pandas as pd
import sys
import os
import datetime
import logging
import datetime
from typing import Optional

def create_logger(
        log_version_name: str,
        logger_name: Optional[str] = 'Log',
        log_path: Optional[str] = '../logs') -> logging.Logger:
    '''Function to create a logger
    
    Examples
    -----------
    >>> logger = create_logger(log_version_name)
    >>> logger.info('Hello World')
    
    Parameters
    ------------
    log_version_name : the name of the log files
    logger_name : if you want to set up different\
        logger, please define its name here
    log_path : directory path of log files
    Returns
    ------------
    logger : logger object
    '''
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=format_str,
                        filename=f'{log_path}/{log_version_name}.log')
    logger = logging.getLogger(logger_name)
    return logger

def main(logger):

    TOP = 200
    dfs = []
    for i in range(TOP):
        df = pd.read_html(f'https://kabutan.jp/warning/?mode=2_1&market=0&capitalization=-1&stc=&stm=0&page={i+1}')
        if df[2].shape[0] == 0:  
            break
        dfs.append(df[2])

    dfs_down = []
    for i in range(TOP):
        df_down = pd.read_html(f'https://kabutan.jp/warning/?mode=2_2&market=0&capitalization=-1&stc=&stm=0&page={i+1}')
        if df_down[2].shape[0] == 0:
            break
        dfs_down.append(df_down[2])

    df_all = pd.concat(dfs, axis=0)
    df_all.reset_index(inplace=True, drop=True)
    df_all = df_all[['コード', '銘柄名', '市場', '株価', 
        '前日比', '前日比.1', '出来高', 'ＰＥＲ', 'ＰＢＲ', '利回り']]
    df_all.columns = ['コード', '銘柄名', '市場', '株価', 
        '前日比_価格差', '前日比_変化率', '出来高', 'PER', 'PBR', '利回り']
    df_all['date'] = datetime.date.today()
    df_all['weekday'] = datetime.date.today().weekday()


    df_all_down = pd.concat(dfs_down, axis=0)
    df_all_down.reset_index(inplace=True, drop=True)
    df_all_down = df_all_down[['コード', '銘柄名', '市場', '株価', 
        '前日比', '前日比.1', '出来高', 'ＰＥＲ', 'ＰＢＲ', '利回り']]
    df_all_down.columns = ['コード', '銘柄名', '市場', '株価', 
        '前日比_価格差', '前日比_変化率', '出来高', 'PER', 'PBR', '利回り']
    df_all_down['date'] = datetime.date.today()
    df_all_down['weekday'] = datetime.date.today().weekday()


    df_all.to_csv(f'./data/{dt}_stock_upranking.csv', index=False)
    df_all_down.to_csv(f'./data/{dt}_stock_downranking.csv', index=False)

    df_all['PER'] = df_all['PER'].apply(lambda x: float(str(x).replace('－','0')))
    df_all['前日比_変化率'] = df_all['前日比_変化率'] = df_all['前日比_変化率'].apply(lambda x: float(x.replace('+', '').replace('%', '')))
    df_all['前日比_価格差'] = df_all['前日比_価格差'].apply(lambda x: float(str(x).replace('+', '').replace(',', '')))
    df_all['出来高'] = df_all['出来高'].apply(lambda x: float(str(x).replace('－', '0')))
    df_all['出来高金額'] = df_all['出来高'] * df_all['株価']
    df_all['有望銘柄フラグ'] = 0
    df_all.loc[df_all.query('出来高金額>=1000000000 & 前日比_変化率>=2 & 前日比_変化率<=4 & PER > 0 & 株価>=1000 & 株価<5000 & 前日比_価格差>50').index ,'有望銘柄フラグ'] = 1
    logger.info(df_all.query('有望銘柄フラグ==1')[['コード', '銘柄名']].values)

if __name__ == '__main__':
    try:
        log_version_name = str(datetime.datetime.now()).replace(
        ' ', '_').replace(':', '_')[:-7] + '_stock_price_bat'
        logger = create_logger(log_version_name, log_path='./logs')

        dt = "{:02d}".format(datetime.date.today().year)\
            +"{:02d}".format(datetime.date.today().month,"00")\
                +"{:02d}".format(datetime.date.today().day, "00")
        logger.info(str(sys.argv[0]))
        main(logger)

    except:
        logger.exception(sys.exc_info())
