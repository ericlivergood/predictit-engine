class Scenario(object):
    def __init__(self, positions):
        self.positions = positions

    def get_return(self):
        total_cost = 0.0 
        total_payout = 0.0 

        for d in self.positions:
            total_cost += d.cost*d.shares
            
            if(d.pays):
                total_payout += d.payout*d.shares

        return (total_payout / total_cost - 1.0) * 100    


    def positionstring(self):
        tickers = []
        for p in self.positions:
            tickers.append(p.ticker)

        return ','.join(tickers)

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

class Market(object):
    def __init__(self, name, market_id, url, type):
        self.name = name
        self.market_id = market_id
        self.url = url
        self.type = type
        self.contracts = []