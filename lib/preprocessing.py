import pandas as pd
import numpy as np
import requests

def data_preprocess(data:dict, **kwargs) -> tuple[list, pd.DataFrame]:
    """
    The data you gather should be parsed in as a dict object, in the format:
    e.g.
    {"AAPL": {pd.DataFrame}
    "TSLA": {pd.DataFrame}}
    The tickers for each data frame act as keys to the data
    """
    tickers = list(data.keys())
    dataframes = list(data.values())
    if len(dataframes) == 1:
        df = data[f'{tickers[0]}'].add_suffix('_'+tickers[0])
        try:
            df.rename(columns={'date_'+tickers[0]: 'timestamp'}, inplace=True)
        except:
            df.rename(columns={'timestamp'+tickers[0]: 'timestamp'}, inplace=True)
        return df.dropna()
    
    df = pd.merge(*dataframes, on='timestamp', how='outer', suffixes=['_'+s for s in tickers])

    return df.dropna()

def df_to_dict(dataframes:list[pd.DataFrame], tickers:list[str]) -> dict:
    if len(tickers) == 1:
        return {tickers[0]: dataframes}
    return {tickers[i]: dataframes[i] for i in range(len(dataframes))}

