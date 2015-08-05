import scrapy
import parsers

class PriceSpider(scrapy.Spider):
    name = "price"
    allowed_domains = ["predictit.org"]
    start_urls = [  'https://www.predictit.org/Home/SingleOption?contractId=1014'  ]

    def parse(self, response):
    	return parsers.parse_contract(response)