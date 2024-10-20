import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Backtest:
    def __init__(self, strategy, data, tickers):
        self.data = data
        self.strategy = strategy()
        self.tickers = tickers
        self.equity = []
        self.positions = pd.DataFrame()
        self.algo_ran = False
    def __prices_to_dict__(self, row):
        return {self.tickers[i]: row[f'close_{self.tickers[i]}'] for i in range(len(self.tickers))}

    def run(self, verbose=0):
        if verbose == 1:
            print(f'Trading {len(self.data)} instances...')
        for index, row in self.data.iterrows():
            for ticker in self.tickers:
                self.strategy.iter(row, ticker) # if multiple tickers, we pass the data for each ticker
            prices = self.__prices_to_dict__(row)
            self.strategy.trader.update_positions(row[f'timestamp'], prices)
            curr_portfolio = self.strategy.trader.account.portfolio_snapshots.iloc[-1]['portfolio']
            self.equity.append(curr_portfolio.tlv)
            self.positions = pd.concat([self.positions, curr_portfolio.positions_to_df(row[f'timestamp'])], axis=0)
            if verbose == 2:
                self.strategy.trader.account._show()
        self.algo_ran = True

    def performance(self):
        """
        Evaluates the performance of the strategy on a few metrics compared with benchmark ()
        begining,
        end,
        duration,
        Total Return,
        Annualized Return,.
        Annualized Volatility,
        Sharpe Ratio,
        Max Drawdown,
        Sortino Ratio,
        Expectation,
        win rate,
        avg trade length,
        """
        if not self.algo_ran:
            raise Exception("Algorithm has not been run yet")
        begin = self.data['timestamp'].iloc[0]  
        end = self.data['timestamp'].iloc[-1]
        duration = end - begin
        
    
    def plot(self):
        if not self.algo_ran:
            raise Exception("Algorithm has not been run yet")
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02)
        for ticker in self.tickers:
            cum_return = (1 + (self.data['close_' + ticker] - self.data['open_' + ticker])/self.data['open_' + ticker]).cumprod()
            fig.add_trace(
                go.Scatter(x=self.data['timestamp'], y=cum_return, mode='lines', name=f'{ticker} Cumulative Returns'),
                row=1, col=1
            )

        
        fig.add_trace(
            go.Scatter(x=self.data[f'timestamp'], y=self.equity, mode='lines', name='Equity'),
            row=2, col=1
        )
        grouped = self.positions.groupby('symbol')
        for name, group in grouped:
            fig.add_trace(
                go.Scatter(x=group['timestamp'], y=group['units'], mode='lines', name=f'{name} units'),
                row=3, col=1
            )
        fig.show()
    