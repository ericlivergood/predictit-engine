from crawlers.items import ContractItem, OfferItem

def parse_contract(response):
    yes = response.css('.offers')[0]
    no = response.css('.offers')[1]
    ticker = response.css('#data td').xpath('text()').extract()[1]

    contract = ContractItem()
    name_selector = response.css('h2')
    if(len(name_selector.css('a')) > 0):
    	name_selector = name_selector.css('a')

    contract['name'] = name_selector.xpath('text()').extract()[0]
    contract['url'] = response.url
    contract['ticker'] = ticker
    contract['buy_yes_offers'] = []
    contract['buy_no_offers'] = []

    def extract(x, i):
        try:
            return x.css('td')[i].xpath('text()').extract()[0]
        except Exception as E:
            return None

    def buildOffer(price, shares):
        if price is None:
        	return 

        oi = OfferItem()
        oi['ticker'] = ticker
        oi['price'] = float(price)/100
        oi['shares'] = int(shares)

        return oi

    i = 0
    for o in yes.css('tbody tr'):
        if i > 0:
            oi = buildOffer(extract(o, 0), extract(o, 1))
            if(oi is not None):
            	contract['buy_yes_offers'].append(oi)
        i += 1

    i = 0
    for o in no.css('tbody tr'):
        if i > 0:
            oi = buildOffer(extract(o, 0), extract(o, 1))
            if(oi is not None):
            	contract['buy_no_offers'].append(oi)
        i += 1
    
    return contract