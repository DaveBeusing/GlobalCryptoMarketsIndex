><b>This repo was checked into Git as part of my cleanup work.</b>

<br>
<br>

# Global Crypto Markets Index (GCMI10)
Very simple/raw Python scripts to create a cryptomarket index.<br>
It uses pandas, altair, sqlalchemy, unicorn_binance_websocket_api, streamlit and the api's from Coingecko and Binance.<br>
Sample data inside the SQLite3 database is from 2022.

### Dependencies
> pip install pandas <br> 
pip install sqlalchemy <br>
pip install streamlit

### Usage
> streamlit run index.py

### api Endpoints
https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc <br>
Binance api is polled via unicorn_binance_websocket_api package

## DISCLAIMER
The Content is for informational purposes only, you should not construe any such information or other material as legal, tax, investment, financial, or other advice.
<br><br>
<b>Please read and understand DISCLAIMER.md in addition to the aforementioned disclaimer.</b>