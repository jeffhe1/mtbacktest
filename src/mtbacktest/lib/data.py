import requests
import pandas as pd
from datetime import datetime as dt
from preprocessing import df_to_dict, data_preprocess, adjust_price
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
API_KEY = os.environ.get('API_KEY')

class Data:
    def __init__(self, api_token=API_KEY, fmt='json'):
        """
        symbols: can be 1 or multiple tickers
        interval, 1m, 5m, 1h, D
        fmt: json, csv
        """
        self.api_token = api_token
        self.fmt = fmt
    
    def __get_max_period__(self, interval:str) -> int:
        if interval == '1m':
            return 120
        if interval == '5m':
            return 600
        if interval == '1h':
            return 7200
        
        return None

    def get_intraday_data(self, symbols, interval, **kwargs):
        max_interval = self.__get_max_period__(interval)
        if max_interval is None:
            raise ValueError('Invalid interval')
        try:
            data_lst = []
            for symbol in symbols:
                url = f"https://eodhd.com/api/intraday/{symbol}.US?interval={interval}&api_token={self.api_token}&fmt={self.fmt}"
                data = pd.DataFrame(requests.get(url).json())
                if data is None:
                    raise ValueError('Incorrect Exchange')
                data_lst.append(data)
            data_dict = df_to_dict(data_lst, symbols)
            data = data_preprocess(data_dict)
            return data
        except Exception as e:
            pass
        
        try:
            data_lst = []
            for symbol in symbols:
                url = f"https://eodhd.com/api/intraday/{symbol}.US?interval={interval}&api_token={self.api_token}&fmt={self.fmt}"
                data = pd.DataFrame(requests.get(url).json())
                if data is None:
                    raise ValueError('Incorrect Exchange')
                data_lst.append(data)
            data_dict = df_to_dict(data_lst, symbols)
            data = data_preprocess(data_dict)
            return data
        except Exception as e:
            pass
        try:
            data_lst = []
            for symbol in symbols:
                url = f"https://eodhd.com/api/intraday/{symbol}.US?interval={interval}&api_token={self.api_token}&fmt={self.fmt}"
                data = pd.DataFrame(requests.get(url).json())
                if data is None:
                    raise ValueError('Incorrect Exchange')
                data_lst.append(data)
            data_dict = df_to_dict(data_lst, symbols)
            data = data_preprocess(data_dict)
            return data
        except Exception as e:
            pass

    def get_daily_data(self, symbols, **kwargs):
        from_date = kwargs.get('from_date', None)
        to_date = kwargs.get('to_date', dt.now().strftime("%Y-%m-%d"))
        if from_date is None:
            try:
                data_lst = []
                for symbol in symbols:
                    url = f"https://eodhd.com/api/eod/{symbol}.US?api_token={self.api_token}&fmt={self.fmt}"
                    data = pd.DataFrame(requests.get(url).json())
                    data = adjust_price(data)
                    if data is None:
                        raise ValueError('Incorrect Exchange')
                    data_lst.append(data)
                df_dict = df_to_dict(data_lst, symbols)
                data = data_preprocess(df_dict)
                return data
            except Exception as e:
                pass

            try:
                data_lst = []
                for symbol in symbols:
                    url = f"https://eodhd.com/api/eod/{symbol}.US?api_token={self.api_token}&fmt={self.fmt}"
                    data = pd.DataFrame(requests.get(url).json())
                    data = adjust_price(data)
                    if data is None:
                        raise ValueError('Incorrect Exchange')
                    data_lst.append(data)
                df_dict = df_to_dict(data_lst, symbols)
                data = data_preprocess(df_dict)
                return data
            except Exception as e:
                pass

            try:
                data_lst = []
                for symbol in symbols:
                    url = f"https://eodhd.com/api/eod/{symbol}.US?api_token={self.api_token}&fmt={self.fmt}"
                    data = pd.DataFrame(requests.get(url).json())
                    data = adjust_price(data)
                    if data is None:
                        raise ValueError('Incorrect Exchange')
                    data_lst.append(data)
                df_dict = df_to_dict(data_lst, symbols)
                data = data_preprocess(df_dict)
                return data
            except Exception as e:
                pass
        if from_date is not None:
            try:
                data_lst = []
                for symbol in symbols:
                    url = f"https://eodhd.com/api/eod/{symbol}.US?api_token={self.api_token}&fmt={self.fmt}"
                    data = pd.DataFrame(requests.get(url).json())
                    data = adjust_price(data)
                    if data is None:
                        raise ValueError('Incorrect Exchange')
                    data_lst.append(data)
                df_dict = df_to_dict(data_lst, symbols)
                data = data_preprocess(df_dict)
                return data
            except Exception as e:
                pass

            try:
                data_lst = []
                for symbol in symbols:
                    url = f"https://eodhd.com/api/eod/{symbol}.US?api_token={self.api_token}&fmt={self.fmt}"
                    data = pd.DataFrame(requests.get(url).json())
                    data = adjust_price(data)
                    if data is None:
                        raise ValueError('Incorrect Exchange')
                    data_lst.append(data)
                df_dict = df_to_dict(data_lst, symbols)
                data = data_preprocess(df_dict)
                return data
            except Exception as e:
                pass

            try:
                data_lst = []
                for symbol in symbols:
                    url = f"https://eodhd.com/api/eod/{symbol}.US?api_token={self.api_token}&fmt={self.fmt}"
                    data = pd.DataFrame(requests.get(url).json())
                    data = adjust_price(data)
                    if data is None:
                        raise ValueError('Incorrect Exchange')
                    data_lst.append(data)
                df_dict = df_to_dict(data_lst, symbols)
                data = data_preprocess(df_dict)
                return data
            except Exception as e:
                pass
        raise Exception("Cannot find symbol")