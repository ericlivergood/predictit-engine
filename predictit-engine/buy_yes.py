import itertools

def evaluate(market):
	if(market.type == 'SingleOption'):
		return

	if(len(market.contracts) == 0):
		return

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
    runningCost = 0.0
    toBuy = []

    for c in market.contracts:
        price = c.cost_to_buy_n_long(n)
        if(price is None):
            return None
        runningCost += price


    if runningCost < n:
        ret = (n-runningCost)/runningCost * .9 #simplified fee calculation
        totalGain = n - runningCost
        return (ret, totalGain, runningCost, n, [])

    return None

    