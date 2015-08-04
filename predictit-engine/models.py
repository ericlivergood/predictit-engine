class Ticker(object):
    def __init__(self, name, ticker, buy_yes, buy_no, sell_yes, sell_no, url, market_id):
        self.name = name
        self.ticker = ticker
        self.buy_yes = buy_yes
        self.buy_no = buy_no
        self.sell_yes = sell_yes
        self.sell_no = sell_no
        self.url = url
        self.market_id = market_id  

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


class Position(object):
    def __init__(self, ticker, cost, shares, payout, pays):
        self.ticker = ticker
        self.cost = cost
        self.shares = shares
        self.payout = payout
        self.pays = pays

class Market(object):
    def __init__(self, name, market_id, url):
        self.name = name
        self.market_id = market_id
        self.url = url