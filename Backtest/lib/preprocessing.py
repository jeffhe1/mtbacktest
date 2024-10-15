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
    df = pd.concat(dataframes, axis=1, keys=tickers)
    return df

