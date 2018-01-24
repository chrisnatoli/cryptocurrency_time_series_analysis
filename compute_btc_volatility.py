import numpy as np
import datetime as dt
import pandas as pd

candles_filename_prefix = 'gdax_btc-usd_candles'
candles_filename_suffix = '_gran60_2017010100-2018012100.csv'
candles = pd.read_csv(candles_filename_prefix + candles_filename_suffix)
candles = candles.set_index('time')
prices = candles['close']
log_returns = np.log(prices).diff().dropna()

days = [ dt.date.fromtimestamp(t) for t in log_returns.index ]
days = sorted(list(set(days)))

volatilities = []
for d in days:
    print(d.strftime('%Y-%m-%d'))
    days_log_returns = []
    for t in log_returns.index:
        if d == dt.date.fromtimestamp(t):
            days_log_returns.append(log_returns[t])
    volatility = np.var(days_log_returns)
    volatilities.append(volatility)

with open('btc_volatility' + candles_filename_suffix, 'w') as fp:
    fp.write('date,volatility\n')
    for i in range(len(days)):
        day_str = days[i].strftime('%Y-%m-%d')
        fp.write(day_str + ',' + str(volatilities[i]) + '\n')
