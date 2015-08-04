import scrapy
import re
from urlparse import urljoin
from crawlers.items import MarketItem, ContractItem, OfferItem

class MarketSpider(scrapy.Spider):
    name = "market"
    allowed_domains = ["predictit.org"]
    start_urls = [
        "https://www.predictit.org/Home/Browse"
    ]

    market_requests = {}
    req_counter = 1

    def add_request(i, r):
        market_id = r.meta['market']['id']
        
        r.meta['req_id'] = MarketSpider.req_counter  

        if(market_id not in MarketSpider.market_requests):
            MarketSpider.market_requests[market_id] = []

        MarketSpider.market_requests[market_id].append(MarketSpider.req_counter)
        MarketSpider.req_counter += 1

    def complete_request(i, r):
        market_id = r.meta['market']['id']
        req_id = r.meta['req_id']
        MarketSpider.market_requests[market_id].remove(req_id)

    def is_complete(i, r):
        market_id = r.meta['market']['id']

        return len(MarketSpider.market_requests[market_id]) == 0

    def parse(self, response):
        callbacks = {
            'SingleOption': self.parseSingleOption,
            'SingleMarket': self.parseSingleMarket
        }
        i = 0
        for market in response.css('.browse-caption2 > .browse-a'):
            try:
                m = MarketItem()
                m['name'] = market.css('h3').xpath('text()').extract()[0]
                m['url'] = urljoin(response.url, market.xpath('@href').extract()[0])
                m['id'] = re.search('marketId=([0-9]*)', m['url']).group(1)
                m['type'] = re.search('/([\w]*)\?', m['url']).group(1)
                m['contracts'] = {}
                
                #markets[m['id']] = m
                r = scrapy.Request(m['url'], callback=callbacks[m['type']])
                r.meta['market'] = m
                MarketSpider.add_request(self, r)
                yield r

            except Exception as E:
                self.logger.info(E)
                self.logger.info(market.extract())
            i += 1
    	
    def parseSingleMarket(self, response):
        MarketSpider.complete_request(self, response)

        for o in response.css('#contractList table')[0].css('.outcome-title'):
            try:
                url = urljoin(response.url, o.xpath('a/@href').extract()[0])

                r = scrapy.Request(url, callback=self.parseSingleOption)
                r.meta['market'] = response.meta['market']
                MarketSpider.add_request(self, r)
                yield r
            except Exception as E:
                self.logger.info(E)
                self.logger.info(o.extract())



    def parseSingleOption(self, response):
        MarketSpider.complete_request(self, response)
        yes = response.css('.offers')[0]
        no = response.css('.offers')[1]
        ticker = response.css('#data td').xpath('text()').extract()[1]

        m = response.meta['market']

        if ticker not in m['contracts']:
            i = ContractItem()
            name_selector = 'h2 a' if(m['type'] == 'SingleMarket') else 'h2'
            i['name'] = response.css(name_selector).xpath('text()').extract()[0]
            i['url'] = response.url
            i['ticker'] = ticker
            i['buy_yes_offers'] = []
            i['buy_no_offers'] = []
            m['contracts'][ticker] = i

        contract = m['contracts'][ticker]

        def extract(x, i):
            try:
                return x.css('td')[i].xpath('text()').extract()[0]
            except Exception as E:
                return None

        def buildOffer(price, shares, yes_no):
            if price is None:
                return 
            oi = OfferItem()
            oi['ticker'] = ticker
            oi['price'] = float(price)/100
            oi['shares'] = int(shares)

            if(yes_no == 'yes'):            
                contract['buy_yes_offers'].append(oi)
            elif(yes_no == 'no'):
                contract['buy_no_offers'].append(oi)

        i = 0
        for o in yes.css('tbody tr'):
            if i > 0:
                buildOffer(extract(o, 0), extract(o, 1), 'yes')
            i += 1

        i = 0
        for o in no.css('tbody tr'):
            if i > 0:
                buildOffer(extract(o, 0), extract(o, 1), 'no')
            i += 1

        if MarketSpider.is_complete(self, response):
            return m
