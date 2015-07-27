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