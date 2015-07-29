from models import Position

def evaluate(market):
	positions = []

	totalCost = 0.0
	totalPositions = 0

	for d in market.data:
		if(d.buy_yes is not None):
			totalCost += d.buy_yes
			totalPositions += 1

	return ((1 - totalCost)/totalCost)
	#return totalCost
