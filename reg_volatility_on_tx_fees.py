import pandas as pd
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt

tx_fee_data = pd.read_csv('data/btc_tx_fee_data.csv').set_index('Date')
tx_fee_series = tx_fee_data['Avg tx fee (BTC)']

volatility_filename = 'data/btc_volatility_gran900_2016010100-2018012303.csv'
df = pd.read_csv(volatility_filename).set_index('date')

df = df.join(tx_fee_series, how='inner')
df['L_volatility'] = df['volatility'].shift(-1)
df = df.rename(columns={'Avg tx fee (BTC)':'txfee'}).dropna()

result = sm.ols(formula='volatility ~ txfee + L_volatility',
                data=df).fit()
# Note: Both BTC-USD daily price and second degree lag on volatility
#       are nonsignificantly correlated with volatility, so I omitted
#       them from the regression.
# Also, plotting all three variables against each other pairwise
# demonstrates no noticeable collinearity.
print(result.summary())
print('\nintercept has beta=' + str(result.params[0])
      + ' with p-value of ' + str(result.pvalues[0]))
print('txfee has beta=' + str(result.params[1])
      + ' with p-value of ' + str(result.pvalues[1]))
print('lag of volatility has beta=' + str(result.params[2])
      + ' with p-value of ' + str(result.pvalues[2]))
