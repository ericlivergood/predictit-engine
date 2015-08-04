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
    def by_short_price(x):
        cost = x.cost_to_buy_n_short(n)

        if cost is None:
            return 2
        return cost

    lastReturn = -10000
    lastGain = -10000
    counter = 0
    runningCost = 0.0
    contracts = sorted(market.contracts, key=by_short_price)
    toBuy = []

    for c in contracts:
        price = c.cost_to_buy_n_short(n)
        if(price is None):
            break

        currentReturn = ((counter)/(runningCost+price)) - 1
        currentGain = currentReturn * (runningCost + price)
        #if(currentReturn < lastReturn):
        #    break
        if(currentGain < lastGain):
            break


        lastReturn = currentReturn
        lastGain = currentGain
        counter += n
        runningCost += price

        toBuy.append(c.ticker)



    if lastReturn > 0:
        lastReturn *= .9 #simplified fee calculation
        totalGain = lastReturn * runningCost 
        return (lastReturn, totalGain, runningCost, n, toBuy)

    return None

    