import pandas as pd
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt

tx_fee_df = pd.read_csv('data/btc_tx_fee_data.csv').set_index('Date')
tx_fee_df = tx_fee_df[['Avg tx fee (BTC)', 'Avg tx fee (USD)']]

volatility_filename = 'data/btc_volatility_gran900_2016010100-2018012303.csv'
df = pd.read_csv(volatility_filename).set_index('date')

df = df.join(tx_fee_df, how='inner')
df['L_volatility'] = df['volatility'].shift(-1)
df = df.rename(columns={'Avg tx fee (BTC)':'txfee_btc',
                        'Avg tx fee (USD)':'txfee_usd'}).dropna()

def reg_volatility_on_txfee(currency):
    print('\nRegressing volatility on tx fee IN ' + currency.upper()
          + ' and lag of volatility:')
    result = sm.ols(formula='volatility ~ txfee_'+currency+' + L_volatility',
                    data=df).fit()
    print(result.summary())
    print('\nIntercept has beta=' + str(result.params[0])
          + ' with p-value of ' + str(result.pvalues[0]))
    print('Tx fee (in ' + currency + ') has beta=' + str(result.params[1])
          + ' with p-value of ' + str(result.pvalues[1]))
    print('Lag of volatility has beta=' + str(result.params[2])
          + ' with p-value of ' + str(result.pvalues[2]))

def plot_collinearity(x_label, y_label):
    plt.scatter(df[x_label], df[y_label], s=1, c='#46711e')
    plt.xlim(0, 1.1*max(df[x_label]))
    plt.ylim(0, 1.1*max(df[y_label]))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig('plots/' + x_label + '_vs_' + y_label + '.png', dpi=300)
    plt.close()

reg_volatility_on_txfee('btc')
reg_volatility_on_txfee('usd')
plot_collinearity('volatility', 'txfee_btc')
plot_collinearity('volatility', 'txfee_usd')
plot_collinearity('volatility', 'L_volatility')
plot_collinearity('txfee_btc', 'L_volatility')
plot_collinearity('txfee_usd', 'L_volatility')
