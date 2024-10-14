import numpy as np
import pandas as pd

class Position:
    def __init__(self, symbol:str, units:float, price:float) -> None:
        self.symbol = symbol
        self.units = units
        self.avg_price = price
        self.curr_price = price
        self.unrealized_pl = 0
        self.realized_pl = 0
        self.status = 'open'
        self.total_value = self.units * self.avg_price
    def _update_position(self, price:float) -> None:
        self.curr_price = price
        self.unrealized_pl = (self.curr_price - self.avg_price) * self.units
        self.total_value = self.units * price
    
    def _add_to_curr_position(self, units:float, price:float) -> None:
        self.avg_price = (self.units * self.avg_price + units * price)/(self.units + units)
        self.units += units
        self.unrealized_pl = (price - self.avg_price) * self.units

    def _close_curr_position(self, price:float, **kwargs) -> None:
        units = kwargs.get('close_units', self.units) # The amount of units you want to close
        self.units -= units
        self.realized_pl = (price - self.avg_price) * units
        self.avg_price = (self.units * self.avg_price) / self.units if self.units != 0 else 0
        self.status = 'closed'
        self._update_position(price)
    
    def _show(self):
        print(f'symbol: {self.symbol}, units: {self.units}, avg_price: {self.avg_price}, curr_price: {self.curr_price}, unrealized_pl: {self.unrealized_pl}, realized_pl: {self.realized_pl}, status: {self.status}, tlv:{self.total_value}')

class Portfolio:
    def __init__(self, positions: set[Position], cash:float):
        self.positions = positions # Note: Positions can be empty
        self.cash = cash # Cash must be initiated by a upper level class method
        self.tlv = sum([pos.total_value for pos in self.positions]) + self.cash
    def _add_position(self, position: Position) -> None:
        dup_pos = [pos for pos in self.positions if pos.symbol == position.symbol]
        cost = position.units * position.avg_price
        self.cash -= cost
        if self.cash < 0:
            self.cash = 0
            raise ValueError('Insufficient cash to buy this position')
        if len(dup_pos) == 1: # There can only be at most 1 duplicate position
            dup = dup_pos[0] # we locate the duplicate position
            dup._add_to_curr_position(position.units, position.avg_price) # We modify the duplicate position

        else:
            self.positions.add(position)
        self.tlv = sum([pos.total_value for pos in self.positions]) + self.cash

    def _close_position(self, symbol:str, price:float, **kwargs) -> None:
        units = kwargs.get('close_units', None)
        try:
            pos = [pos for pos in self.positions if pos.symbol == symbol][0]
        except IndexError:
            raise ValueError('Position does not exist in the portfolio')
        if pos.status == 'closed':
            raise ValueError('Position is already closed')
        if units is not None:
            pos._close_curr_position(price, close_units=units)
            close_size = units * price
        else:
            pos._close_curr_position(price)
            close_size = pos.total_value
        self.cash += close_size
        self.tlv = sum([pos.total_value for pos in self.positions]) + self.cash
    def _update_portfolio(self, prices:dict) -> None:
        for pos in self.positions:
            pos._update_position(prices[pos.symbol])
        self.tlv = sum([pos.total_value for pos in self.positions]) + self.cash
    def _show(self):
        for pos in self.positions:
            pos._show()
        print(f'Cash: {self.cash},\nTotal Value: {self.tlv}\n')
    

class Account:
    def __init__(self, id:int, cash:float, portfolio:Portfolio):
        self.id = id
        pass
        

class Strategy:
    def __init__(self):
        pass

if __name__ == '__main__':
    portfolio = Portfolio(set(), 100000)
    position = Position('AAPL', 10, 100)
    portfolio._add_position(position)
    portfolio._add_position(Position('AAPL', 10, 110))
    portfolio._add_position(Position('TSLA', 10, 200))
    portfolio._show()
    portfolio._close_position("AAPL", 95, close_units=10)
    new_prices = {'AAPL': 90, 'TSLA': 210}
    portfolio._update_portfolio(new_prices)
    portfolio._show()
    new_prices = {'AAPL': 91, 'TSLA': 215}
    portfolio._update_portfolio(new_prices)
    portfolio._show()
    new_prices = {'AAPL': 91, 'TSLA': 300}
    portfolio._update_portfolio(new_prices)
    portfolio._show()
    
    