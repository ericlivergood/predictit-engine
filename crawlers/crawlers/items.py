import scrapy

class MarketItem(scrapy.Item):
	name = scrapy.Field()
	url = scrapy.Field()
	id = scrapy.Field()
	type = scrapy.Field()
	contracts = scrapy.Field()

class ContractItem(scrapy.Item):
	name = scrapy.Field()
	url = scrapy.Field()
	ticker = scrapy.Field()
	buy_yes_offers = scrapy.Field()
	buy_no_offers = scrapy.Field()

class OfferItem(scrapy.Item):
	ticker = scrapy.Field()
	price = scrapy.Field()
	shares = scrapy.Field()

