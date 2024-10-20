import numpy as np
import pandas as pd

class Backtest:
    def __init__(self, strategy, data, tickers):
        self.data = data
        self.strategy = strategy()
        self.tickers = tickers

    def __prices_to_dict__(self, row):
        return {self.tickers[i]: row[f'close_{self.tickers[i]}'] for i in range(len(self.tickers))}

    def run(self, verbose=False):
        for index, row in self.data.iterrows():
            self.strategy.iter(row)
            prices = self.__prices_to_dict__(row)
            self.strategy.strategy.update_positions(row[f'timestamp_{self.tickers[0]}'], prices)
            if verbose:
                self.strategy.strategy.account._show()
            
if __name__ == '__main__':    
    from backtest import Backtest
    from lib.simulation import simulate_GBM
    from lib.preprocessing import data_preprocess, df_to_dict
    import pandas as pd
    from strategy import Strategy

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

    data = pd.read_json('test_data1.json')
    data['dreturn'] = ((data['close'] - data['open'])/data['open']) * 100
    data = data.iloc[-100:]
    data = df_to_dict(data, ['AAPL'])
    data = data_preprocess(data)
    bt = Backtest(DummyStrat, data, ['AAPL'])
    bt.run(verbose=True)
