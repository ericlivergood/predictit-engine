import buy_no
from models import Market, Contract, Offer

def test_evaluate_empty_market():
    market = Market('test', 0, '', 'SingleOption')
    market.contracts = []

    r = buy_no.evaluate(market)
    assert (r is None)

def test_evaluate_profitable():
    market = Market('test', 0, '', 'SingleOption')
    c1 = Contract('test', 'test1', '')
    c2 = Contract('test', 'test2', '')
    c3 = Contract('test', 'test3', '')

    c1.short_offers = [ Offer(c1, 'NO', .4, 10) ]
    c2.short_offers = [ Offer(c2, 'NO', .6, 10) ]
    c3.short_offers = [ Offer(c3, 'NO', .8, 10) ]


    market.contracts = [ c1, c2, c3 ]

    r = buy_no.evaluate(market)
    
    assert r is not None

    ret = r[0]
    gain = r[1]
    cost = r[2]
    shares = r[3]

    assert cost == 18
    assert shares == 10
    assert round(ret, 2) == .1
    assert round(gain, 2) == 1.8


class Expando(object):
    pass