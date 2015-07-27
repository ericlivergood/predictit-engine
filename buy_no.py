import itertools
from position import Position
from scenario import Scenario
def evaluate(market):

    maxReturn = (None, None, -1000)

    for c in _generate_scenarios(market.data):
        for w in c.positions:
            ret = _evaluate_scenario(c, w)
            if(ret > maxReturn[2]):
                maxReturn = (c,w,ret)

    #_print_scenario(maxReturn[0], maxReturn[1])
    #print('Return: ' + str(maxReturn[2]))
    #print('')

    return maxReturn

def _generate_combinations(data):
    positions = []
    for d in data:
        if(d.buy_no is not None):
            positions.append(Position(d.ticker, d.buy_no, 1, 1.0, True))

    r = len(positions)
    while r > 1:
        for c in itertools.combinations(positions, r):
            yield Scenario(c)
        r -= 1

def _generate_scenarios(data):
    positions = []

    for d in data:
        if(d.buy_no is not None):
            positions.append(Position(d.ticker, d.buy_no, 1, 1.0, True))

    positions = sorted(positions, key=lambda x: x.cost, reverse = False)
    
    i = len(positions)

    while(i > 1):
        yield Scenario(list(_top_n(positions, i)))
        i -=1

def _top_n(positions, n):
    i = 1    
    for p in positions:
        if(i <= n):
            yield p
        i += 1


def _evaluate_scenario(scenario, winner):
    for p in scenario.positions:
        if(p.ticker == winner.ticker):
            p.pays = False
        else:
            p.pays = True
    ret = scenario.get_return()

    return ret

def _print_scenario(scenario, winner):
    print('Positions: ' + scenario.positionstring())
    print('Winner ' + winner.ticker)