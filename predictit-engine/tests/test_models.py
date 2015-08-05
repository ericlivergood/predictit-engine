from models import Contract, Offer

def test_contract_costs():
	c = Contract('ticker', 'test', '')
	c.long_offers = [
		Offer(c, 'Yes', .1, 5),
		Offer(c, 'Yes', .16, 10),
		Offer(c, 'Yes', .2, 100),
	]

	c.short_offers = [
		Offer(c, 'Yes', .4, 6),
		Offer(c, 'Yes', .5, 4),
		Offer(c, 'Yes', .6, 10),
	]

	assert c.cost_to_buy_n_long(1000) is None
	assert c.cost_to_buy_n_short(1000) is None

	assert c.cost_to_buy_n_long(5) == .5
	assert c.cost_to_buy_n_long(10) == 1.3
	assert c.cost_to_buy_n_long(20) == 3.1

	assert c.cost_to_buy_n_short(6) == 2.4
	assert c.cost_to_buy_n_short(10) == 4.4
	assert c.cost_to_buy_n_short(12) == 5.6
	assert c.cost_to_buy_n_short(20) == 10.4
