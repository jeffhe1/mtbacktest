# Backtest
Custom backtest framework
An example multi-ticker strategy (long short)
```python
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

```