

import requests
import pandas as pd


url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"

request = requests.get(url)

df = pd.DataFrame( request.json() )

symbols = ['btc', 'eth', 'bnb', 'xrp', 'ada','sol','dot','luna','AVAX','doge','shib','matic','ltc','atom','link','near','trx','algo','bch','ftt','xlm','ftm','uni','mana','hbar','sand','etc','axs','icp','vet','xtz','fil','egld','theta','xmr','klay','hnt','grt','gala','one','eos', 'flow','aave','cake','mkr','qnt','enj','ar','tfuel','xec','stx','neo','ksm','zec','amp','rune', 'cvx','bat','celo','lrc','crv','rose','chz','dash','waves','scrt','slp','snx','mina']


#top_10 = df[ df.symbol.isin( symbols ) ].nlargest( 10, 'market_cap' ).symbol.to_list()
#print( top_10 )



top_10 = ['btc', 'eth', 'bnb', 'ada', 'xrp', 'sol', 'doge', 'dot', 'trx', 'shib']

data = df[ df.symbol.isin( top_10 ) ].nlargest( 10, 'market_cap' )



rawdata = { 
    "symbol" : data['symbol'], 
    "name" : data['name'],
    "price" : data['current_price'],
    "market_cap" : data['market_cap']
}


indexdata = pd.DataFrame(rawdata)
#indexdata = indexdata.astype({"price": float})
#indexdata.reset_index(drop=True)

print(indexdata)
print(indexdata.market_cap)
#print(indexdata.market_cap.values[0])