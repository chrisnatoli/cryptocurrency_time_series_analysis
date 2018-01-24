import pandas as pd
import numpy as np
import quandl


with open('quandl_api_key') as fp:
    quandl.ApiConfig.api_key = fp.read().strip()

total_tx_fees = quandl.get('BCHAIN/TRFEE')
total_tx_fees.rename(columns={'Value':'Total tx fees (BTC)'},
                              inplace=True)

num_txs = quandl.get('BCHAIN/NTRAN')
num_txs.rename(columns={'Value':'Num txs'},
                        inplace=True)

df = total_tx_fees.join(num_txs)
df['Avg tx fee (BTC)'] = df['Total tx fees (BTC)'] / df['Num txs']

btc_usd = quandl.get('BCHAIN/MKPRU')
btc_usd.rename(columns={'Value':'BTC-USD'}, inplace=True)
df = df.join(btc_usd)
df['Avg tx fee (USD)'] = df['Avg tx fee (BTC)'] * df['BTC-USD']

df = df['20130101':]

df.to_csv('btc_transaction_fee_data.csv')
