import json
import urllib
from models import Market, Ticker

def get_predictit_markets(from_file=None):
    if(from_file is not None):
        raw = json.loads(open(from_file).read())
        #GET https://www.kimonolabs.com/api/1z8qa6p4?apikey=73b982d2afa7f55abf54216505965f11&kimmodify=1    
    else:
        raw = json.load(urllib.urlopen("https://www.kimonolabs.com/api/1z8qa6p4?apikey=73b982d2afa7f55abf54216505965f11&kimmodify=1"))

    results = []

    for r in raw['results']['collection1']:
        results.append(Market(r['title'], r['marketId']));

    return results


def get_predictit_marketdata(from_file=None):
    if(from_file is not None):
        raw = json.loads(open(from_file).read())
        #GET https://www.kimonolabs.com/api/bzvl9p4e?apikey=73b982d2afa7f55abf54216505965f11&kimmodify=1
    else:
        raw = json.load(urllib.urlopen("https://www.kimonolabs.com/api/bzvl9p4e?apikey=73b982d2afa7f55abf54216505965f11&kimmodify=1"))

    results = {}

    for r in raw['results']['collection1']:
        try: 
            x = _decode_ticker_json(r)
            i = x.market_id

            if(i not in results):
                results[i] = []
            results[i].append(x)
        except:
            print('failed to decode: ' + str(r))
    return results


def _decode_ticker_json(data):
    return Ticker(name = data['name']['text'], 
        ticker = data['ticker']['text'], 
        buy_yes = _parse_price(data['buy_yes']),
        buy_no = _parse_price(data['buy_no']),
        sell_yes = _parse_price(data['sell_yes']),
        sell_no = _parse_price(data['sell_no']),
        url = data['url'],
        market_id = data['marketId']
    )

def _parse_price(price):
    if price == 'None' or price is None:
        return None
    else:
        return float(price)/100



