import itertools

def evaluate(market):
    start = 1
    step = 1
    n = step + start

    current = _evaluate_for_n_shares(market, start)
    
    next = _evaluate_for_n_shares(market, n)

    while(current is not None and next is not None):
        if(next[1] <= current[1]):
            break

        n+=step
        current = next
        next = _evaluate_for_n_shares(market, n)

    return current

def _evaluate_for_n_shares(market, n):

    cost = 0.0
    value = 0.0
    toBuy = []

    for c in market.contracts:
        p = _evaluate_contract(c, n)

        if(p is not None and p < n):
            value += n
            cost += p
            toBuy.append(c.ticker)


    
    if(len(toBuy) > 0):
        totalReturn = (value-cost)/cost * .9
        totalGain = value-cost
        return (totalReturn, totalGain, cost, n, toBuy)


def _evaluate_contract(contract, n):
    long_price = contract.cost_to_buy_n_long(n)
    short_price = contract.cost_to_buy_n_short(n)

    if(long_price is not None and short_price is not None):
        return long_price + short_price

    return None

    