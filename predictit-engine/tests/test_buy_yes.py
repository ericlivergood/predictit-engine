import buy_yes
from models import Market, Contract, Offer

def test_evaluate_empty_market():
    market = Market('test', 0, '', 'SingleMarket')
    market.contracts = []

    r = buy_yes.evaluate(market)
    assert (r is None)

def test_evaluate_profitable():
    market = Market('test', 0, '', 'SingleMarket')
    c1 = Contract('test', 'test1', '')
    c2 = Contract('test', 'test2', '')
    c3 = Contract('test', 'test3', '')

    c1.long_offers = [ Offer(c1, 'YES', .1, 10) ]
    c2.long_offers = [ Offer(c2, 'YES', .2, 10) ]
    c3.long_offers = [ Offer(c3, 'YES', .3, 10) ]


    market.contracts = [ c1, c2, c3 ]

    r = buy_yes.evaluate(market)
    
    assert r is not None

    ret = r[0]
    gain = r[1]
    cost = r[2]
    shares = r[3]

    assert cost == 6
    assert shares == 10
    assert round(ret, 2) == .6
    assert round(gain, 2) == 4


def test_evaluate_notprofitable():
    market = Market('test', 0, '', 'SingleMarket')
    c1 = Contract('test', 'test1', '')
    c2 = Contract('test', 'test2', '')
    c3 = Contract('test', 'test3', '')

    c1.long_offers = [ Offer(c1, 'YES', .4, 10) ]
    c2.long_offers = [ Offer(c2, 'YES', .5, 10) ]
    c3.long_offers = [ Offer(c3, 'YES', .6, 10) ]



    market.contracts = [ c1, c2, c3 ]

    r = buy_yes.evaluate(market)
    
    assert r is None
