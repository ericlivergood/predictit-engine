class Offer(object):
    def __init__(self, contract, type, price, shares):
        self.contract = contract
        self.type = type
        self.price = price
        self.shares = shares

class Contract(object):
    def __init__(self, ticker, name, url):
        self.ticker = ticker
        self.name = name
        self.url = url
        self.long_offers = []
        self.short_offers = []

    def cost_to_buy_n_short(self, n):
        return self._cost_to_buy_n(n, self.short_offers)

    def cost_to_buy_n_long(self, n):
        return self._cost_to_buy_n(n, self.long_offers)

    def _cost_to_buy_n(self, n, offers):
        bought = 0
        cost = 0.0
        level = 0
        while(bought < n and level < len(offers)):
            current = offers[level]

            if(current.shares + bought >= n):
                return round(cost + (n-bought)*current.price,2)
            else:
                bought += current.shares
                cost += current.shares * current.price
            level += 1

        return None



class Market(object):
    def __init__(self, name, market_id, url, type):
        self.name = name
        self.market_id = market_id
        self.url = url
        self.type = type
        self.contracts = []