#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) Dave Beusing <david.beusing@gmail.com>
#
#

import requests

import streamlit as st
import pandas as pd
import altair as alt


from sqlalchemy import create_engine

engine = create_engine('sqlite:///GCMI10.sqlite3')

top_10 = ['btc', 'eth', 'bnb', 'ada', 'xrp', 'sol', 'doge', 'dot', 'trx', 'shib']
top_10u = [ symbol.upper() for symbol in top_10 ]

def calculateIndex( cryptolist ):
    returns = []    
    for coin in cryptolist:
        df = pd.read_sql( ( coin + 'usdt' ).upper(), engine )
        ret = df.close_price.pct_change() / len( cryptolist )
        ret.index = pd.to_datetime( df.kline_close_time, unit='ms' )
        returns.append( ret ) 
    retframe = pd.concat( returns, axis=1 )
    indexseries = round( 1000 * ( 1 + retframe.sum( axis=1 ) ).cumprod() ,2)
    indexseries.name = 'BPS'
    return indexseries

def calculateBPS( obj ):
    lastval = stobj.BPS.iloc[-2]
    currval = stobj.BPS.iloc[-1]
    diffval = currval - lastval
    delta = round( currval - 1000, 2)
    delta_diff = round( (lastval -1000) - delta, 2)
    bips = {
        "last" : lastval,
        "current" : currval,
        "diff" : diffval,
        "delta" : delta,
        "deltadiff" : delta_diff
    }
    return bips

def indexedAssets( cryptolist ):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
    request = requests.get(url)
    df = pd.DataFrame( request.json() )
    data = df[ df.symbol.isin( cryptolist ) ].nlargest( 10, 'market_cap' )
    rawdata = { 
        "symbol" : data['symbol'], 
        "name" : data['name'],
        "price" : data['current_price'],
        "market_cap" : data['market_cap']
    }
    assets = pd.DataFrame(rawdata)
    assets = assets.astype({"price": float})
    assets = assets.astype({"market_cap": float})
    assets.reset_index(drop=True)
    return assets

def chartCreator( data ):
    #chart = alt.Chart( obj ).mark_line().encode(x='kline_close_time', y=alt.Y('BPS', scale=alt.Scale(domain=[obj.BPS.min(), obj.BPS.max()]))).properties(width=800)
    #return chart.interactive()
    hover = alt.selection_single(
        fields=["kline_close_time"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    lines = (
        alt.Chart(data, title="Top 10 Crypto Assets by USD Market Capitalization")
        .mark_line()
        .encode(
            x="kline_close_time",
            y=alt.Y('BPS', scale=alt.Scale(domain=[data.BPS.min(), data.BPS.max()]))
        )
        .properties(width=800)
    )
    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)
    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="kline_close_time",
            y="BPS",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("kline_close_time", title="Date"),
                alt.Tooltip("BPS", title="Basis Points"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()


#######


stobj = calculateIndex( top_10u ).reset_index()
bps = calculateBPS( stobj )
assets = indexedAssets( top_10u )

st.set_page_config(
    page_title='GCMI10 - Global Crypto Markets Index'
)

if st.button('Update'):
    stobj = calculateIndex( top_10 ).reset_index()
    bps = calculateBPS( stobj )
    assets = indexedAssets( top_10 )

st.header('Global Crypto Markets Index (GCMI10)')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Basis Points (BPS)', round(bps["current"], 2), round(bps["diff"], 2))
col2.metric('BPS Delta', bps['delta'], bps['deltadiff'], delta_color='inverse')
col3.metric('BPS High', stobj.BPS.max())
col4.metric('BPS Low', stobj.BPS.min())
col5.metric('BPS Spread', round( ( stobj.BPS.min() - stobj.BPS.max()) , 2 ) )
st.altair_chart( chartCreator(stobj) )
st.subheader( 'Indexed Assets (USDT)' )
st.write( assets )


st.text('(c) 2022 BSNG Capital Management | hello@bsng.eu \n\n The Content is for informational purposes only,\n you should not construe any such information or other material as legal,\n tax, investment, financial, or other advice.')