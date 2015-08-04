#import kimono
import buy_no#, buy_yes
import json
import io
from models import Market, Contract, Offer


def load(path):
    raw = json.loads(open(path).read())
    markets = []
    for r in raw:
        m = Market(r['name'], r['id'], r['url'], r['type'])
        if('contracts' in r):
            for x in r['contracts'].keys():
                rc = r['contracts'][x]

                c = Contract(x, rc['name'], rc['url'])

                for z in rc['buy_yes_offers']:
                    o = Offer(c, 'buy_yes', z['price'], z['shares'])
                    c.long_offers.append(o)
                for z in rc['buy_no_offers']:
                    o = Offer(c, 'buy_no', z['price'], z['shares'])
                    c.short_offers.append(o)

                c.long_offers=sorted(c.long_offers, key=lambda x: x.price)
                c.short_offers=sorted(c.short_offers, key=lambda x: x.price)
                m.contracts.append(c)
            markets.append(m)
    return markets




def evaluate_all(markets):
    for m in markets:
        #if(m.market_id == '1232'):
        if(1==1):
            x = buy_no.evaluate(m)
            if(x is not None and x[0] > 0):
                print(m.name +'('+m.market_id+')')
                print('-------------------------------------------')
                print('Return: $'+str(x[1]) + ' ('+str(x[0]*100)+'%)')
                print('Cost: $'+str(x[2]) + ', ' + str(x[3]) + ' shares')
                print ('Tickers: ' + ','.join(x[4]))
                print ('')

#evaluate_all(load())
evaluate_all(load('data/scrapy.json'))