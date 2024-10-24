import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from examples import DummyStrat, MultiTickerDummyStrat
from lib.preprocessing import data_preprocess , df_to_dict
class Backtest:
    def __init__(self, strategy, data, tickers):
        self.data = data
        self.strategy = strategy()
        self.tickers = tickers
        self.equity = []
        self.positions = pd.DataFrame()
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
            if curr_portfolio.tlv < 1:
                self.equity.append(0)
                continue      
            self.equity.append(curr_portfolio.tlv)
            self.positions = pd.concat([self.positions, curr_portfolio.positions_to_df(row[f'timestamp'])], axis=0)
            if verbose == 2:
                self.strategy.trader.account._show()
    
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

if __name__ == '__main__':
    from strategy import Strategy
    from backtest import Backtest
    from lib.preprocessing import df_to_dict, data_preprocess
    import pandas as pd
    import numpy as np

    class DummyStrat():
        def __init__(self):
            self.strategy = Strategy()
            self.account = self.strategy.account
            def signal(dreturn):
                if dreturn > 2:
                    return 1
                if dreturn < -2:
                    return -1
                return 0
            self.signal_func= signal
        
        def iter(self, data):
            curr_signal = self.signal_func(data['dreturn_AAPL'])
            units = (self.account.buying_power // 2)/data['close_AAPL']
            curr_portfolio = self.account.portfolio_snapshots.iloc[-1]['portfolio']
            open_positions = [pos for pos in curr_portfolio.positions if pos.symbol == 'AAPL' and pos.status == 'open']
            if curr_signal == 1:
                '''
                We long equity
                '''
                if len(open_positions) == 0:
                    self.strategy.create_position(data['timestamp_AAPL'], 'AAPL', units, data['close_AAPL'])
            
            elif curr_signal == -1:
                '''
                We short equity
                '''
                if len(open_positions) == 0:
                    self.strategy.create_position(data['timestamp_AAPL'], 'AAPL', -units, data['close_AAPL'])

            elif curr_signal == 0 and len(open_positions) > 0:
                '''
                We close position
                '''
                self.strategy.close_position(data['timestamp_AAPL'], 'AAPL', data['close_AAPL'])
    class MultiTickerDummyStrat():
        def __init__(self):
            self.strategy = Strategy()
            self.account = self.strategy.account
            def signal(dreturn):
                if dreturn > 2:
                    return 1
                if dreturn < -2:
                    return -1
                return 0
            self.signal_func= signal
        
        def iter(self, data, ticker):
            curr_signal = self.signal_func(data['dreturn_' + ticker])
            units = (self.account.buying_power // 3)/data['close_' + ticker]
            curr_portfolio = self.account.portfolio_snapshots.iloc[-1]['portfolio']
            open_positions = [pos for pos in curr_portfolio.positions if pos.symbol == ticker and pos.status == 'open']
            if curr_signal == 1:
                '''
                We long equity
                '''
                if len(open_positions) == 0:
                    self.strategy.create_position(data['timestamp'], ticker, units, data['close_'+ticker])
            
            elif curr_signal == -1:
                '''
                We short equity
                '''
                if len(open_positions) == 0:
                    self.strategy.create_position(data['timestamp'], ticker, -units, data['close_'+ticker])

            elif curr_signal == 0 and len(open_positions) > 0:
                '''
                We close position
                '''
                self.strategy.close_position(data['timestamp'], ticker, data['close_'+ticker])

    data = pd.read_json('test_data1.json')
    data2 = pd.read_json('test_data2.json')
    data['dreturn'] = ((data['close'] - data['open'])/data['open']) * 100
    data2['dreturn'] = ((data2['close'] - data2['open'])/data2['open']) * 100
    data2 = data2.iloc[-100:]
    data = data.iloc[-100:]
    data = df_to_dict([data, data2], ['AAPL', 'TSLA'])
    data = data_preprocess(data)
    bt = Backtest(MultiTickerDummyStrat, data, ['AAPL', 'TSLA'])
    bt.run(verbose=True)
    