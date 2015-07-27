import kimono
import buy_no


def load():
    markets = kimono.get_predictit_markets()
    marketdata = kimono.get_predictit_marketdata()

    for m in markets:
        m.data = marketdata[m.market_id]

    return markets

def evaluate_all(markets):
    for m in markets:
        #if(m.market_id == '1232'):
        if(1==1):
            x = buy_no.evaluate(m)
            if(x[0] is not None and x[2] > 0):
                print(m.name +'('+m.market_id+')')
                print('-------------------------------------------')
                print('Max: '+str(x[2])+'%')
                print ('Tickers: ' + x[0].positionstring())
                print ('')

evaluate_all(load())