# cryptocurrency_time_series_analysis

Assorted scripts for statistical analysis of cyrptocurrencies 

### compute_btc_volatility.py

Uses BTC/USD candles in given period of time at given granularity (i.e.,
timescale) to compute the volatility each day in the given period of time,
where volatility is the variance of log(price[t]/price[t-1]).

### get_btc_tx_fee_data.py

Uses Quandl's API to collect data on BTC transaction fees and compute average
transaction fee per day in terms of BTC and USD.

### get_gdax_historic_data.py

Uses GDAX's API to get crypto/USD candles at given granularity (i.e.,
timescale) in given period of time.

### get_korbit_historic_data.py

Uses Korbit's API to get hourly BTC/KRW candles in given period of time.

### reg_volatility_on_tx_fees.py

Regresses daily volatility in BTC/USD on average transaction fee that day and
the previous day's volatility. Prints regression summaries and produces
diagnostic plots for collinearity. Analysis is written up
[here](https://nato.li/blog/do-higher-bitcoin-transaction-fees-lead-to-higher-volatility).
