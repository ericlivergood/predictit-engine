import buy_no

def test_evaluate_empty_market():
    market = Expando()
    market.data = []

    r = buy_no.evaluate(market)
    assert (r[2] == -1000)


l = [1,2,3,4,5,6]

def test_top_n_one_item():
    top = buy_no._top_n(l, 1)
    assert (list(top) == [1])

def test_top_n_some_items():
    top = buy_no._top_n(l, 3)
    assert (list(top) == [1,2,3])

def test_top_n_all_items():
    top = buy_no._top_n(l, len(l))
    assert (list(top) == l)    


class Expando(object):
    pass