import buy_yes_no
from models import Market, Contract, Offer

def test_evaluate_empty_market():
    market = Market('test', 0, '', 'SingleMarket')
    market.contracts = []

    r = buy_yes_no.evaluate(market)
    assert (r is None)

def test_evaluate_profitable():
    market = Market('test', 0, '', 'SingleMarket')
    c1 = Contract('test', 'test1', '')

    c1.long_offers = [ Offer(c1, 'YES', .4, 10) ]
    c1.short_offers = [ Offer(c1, 'NO', .4, 5)]

    market.contracts = [ c1 ]

    r = buy_yes_no.evaluate(market)
    
    assert r is not None

    ret = r[0]
    gain = r[1]
    cost = r[2]
    shares = r[3]

    assert shares == 5
    assert cost == 4
    assert round(ret, 2) == .23
    assert round(gain, 2) == 1


def test_evaluate_notprofitable():
    market = Market('test', 0, '', 'SingleMarket')
    c1 = Contract('test', 'test1', '')

    c1.long_offers = [ Offer(c1, 'YES', .52, 10) ]
    c1.short_offers = [ Offer(c1, 'NO', .54, 5)]


    market.contracts = [ c1 ]

    r = buy_yes_no.evaluate(market)
    
    assert r is None
