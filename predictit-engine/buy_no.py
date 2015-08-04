import itertools


def evaluate(market):

    def by_short_price(x):
        if len(x.short_offers) == 0:
            return 2
        return x.short_offers[0]

    lastReturn = -10000
    minShares = 10000
    counter = 0
    runningCost = 0.0
    contracts = sorted(market.contracts, key=by_short_price)
    toBuy = []

    for c in contracts:
        if(len(c.short_offers) == 0):
            break

        offer = c.short_offers[0]

        currentReturn = ((counter)/(runningCost+offer.price)) - 1

        if(currentReturn < lastReturn):
            break

        lastReturn = currentReturn
        counter += 1
        runningCost += offer.price
        if(offer.shares < minShares):
            minShares = offer.shares

        toBuy.append(c.ticker)



    if lastReturn > 0:
        totalCost = runningCost*minShares
        totalGain = lastReturn * totalCost
        return (lastReturn, totalGain, totalCost, minShares, toBuy)
    return None

    