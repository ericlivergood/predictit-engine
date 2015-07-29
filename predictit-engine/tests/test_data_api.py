import kimono

#slow tests that hit the API
#def test_get_markets():
#	data = kimono.get_predictit_markets()
#	assert True

#def test_get_marketdata():
#	data = kimono.get_predictit_marketdata()
#	assert True
#

def test_parse_markets():
	data = kimono.get_predictit_markets('../data/markets.json')
	assert True

def test_parse_marketdata():
	data = kimono.get_predictit_marketdata('../data/marketdata.json')
	assert True

def test_ticker_decode():
	data = {
		'name':{'href':'https://www.predictit.org/Home/SingleOption?contractId=574','text':'Democratic'},
		'ticker':{'href':'https://www.predictit.org/Home/SingleOption?contractId=574','text':'DEM.CALSEN16'},
		'buy_yes':'95',
		'sell_yes':'91',
		'buy_no':'9',
		'sell_no':'5',
		'index':7,
		'url':'https://www.predictit.org/Home/SingleMarket?marketId=1306#sthash.6QbswLPc.dpbs',
		'marketId':'1306'
	}
	t = kimono._decode_ticker_json(data)

	assert t.name == 'Democratic'
	assert t.ticker == 'DEM.CALSEN16'
	assert t.buy_yes == .95
	assert t.sell_yes == .91
	assert t.buy_no == .09
	assert t.sell_no == .05
	assert t.market_id == '1306'

def test_price_parser():
	assert kimono._parse_price('None') == None
	assert kimono._parse_price('100') == 1
	assert kimono._parse_price('0') == 0
	assert kimono._parse_price('50') == .50
	assert kimono._parse_price(None) == None
	assert kimono._parse_price(100) == 1
	assert kimono._parse_price(0) == 0
	assert kimono._parse_price(50) == .50

