import scrapy
import re
import parsers
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

        MarketSpider.complete_request(self, response)



    def parseSingleOption(self, response):
        i = parsers.parse_contract(response)
        m = response.meta['market']

        m['contracts'][i['ticker']] = i
        MarketSpider.complete_request(self, response)

        if MarketSpider.is_complete(self, response):
            return m
