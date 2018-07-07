def fill_model(symbol):
    data = []
    return data[symbol]['Close']

class Backtest:
    def __init__(self, starting_balance=100000):
        self.balance = starting_balance
        self.positions = {}
        self.balances = {}

    def place_order(self, symbol, quantity, side, order_type, id, limit_price=None):
        if order_type == 'market':
            try:
                if side == 'buy':
                    price = fill_model(symbol=symbol)
                    self.positions[symbol]['quantity'][id] = self.positions[symbol]['quantity'] + quantity
                    self.balance -= quantity * price
                    self.balances[symbol][id] = self.balance
                else:
                    price = fill_model(symbol=symbol)
                    self.positions[symbol]['quantity'][id] = self.positions[symbol]['quantity'] - quantity
                    self.balance += quantity * price
                    self.balances[symbol][id] = self.balance
            except:
                self.positions[symbol] = {}
                if side == 'buy':
                    self.positions[symbol]['quantity'] = quantity
                elif side == 'sell':
                    self.positions[symbol]['quantity'] = -quantity
        if order_type == 'limite':
            print()

    def get_positions(self, symbol):
        try:
            return self.positions[symbol]
        except:
            return None

    def get_balances(self, symbol):
        try:
            return self.balances[symbol]
        except:
            return None
