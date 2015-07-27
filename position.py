class Position(object):
    def __init__(self, ticker, cost, shares, payout, pays):
        self.ticker = ticker
        self.cost = cost
        self.shares = shares
        self.payout = payout
        self.pays = pays