import pandas as pd
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt

tx_fee_df = pd.read_csv('data/btc_tx_fee_data.csv').set_index('Date')
tx_fee_df = tx_fee_df[['Avg tx fee (BTC)', 'Avg tx fee (USD)', 'Num txs']]

volatility_filename='data/btc_volatility_gran900_2016010100-2018012303.csv'
df = pd.read_csv(volatility_filename).set_index('date')

df = df.join(tx_fee_df, how='inner')
df['L_volatility'] = df['volatility'].shift(-1)
df = df.rename(columns={'Avg tx fee (BTC)':'txfee_btc',
                        'Avg tx fee (USD)':'txfee_usd',
                        'Num txs':'num_txs'}).dropna()
print('Data spans from ' + df.index[0] + ' to ' + df.index[-1])
print(str(len(df.index)) + ' datapoints')

def reg_volatility_on_txfee(currency):
    print('\nRegressing volatility on tx fee IN ' + currency.upper()
          + ' and lag of volatility:')
    result = sm.ols(formula = 'volatility ~ txfee_'
                              + currency + ' + L_volatility + num_txs',
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
plot_collinearity('volatility', 'num_txs')
plot_collinearity('txfee_btc', 'L_volatility')
plot_collinearity('txfee_usd', 'L_volatility')
plot_collinearity('txfee_usd', 'num_txs')
plot_collinearity('txfee_btc', 'num_txs')

# Also plot volatility over time; I'm curious.
plt.plot(range(len(df.index)), df['volatility'],
         color='#46711e', linewidth=0.5)
ax = plt.gca()
monthly_labels = [d for d in df.index.values if d[8:10]=='01']
corresponding_ticks = [df.index.values.tolist().index(d)
                       for d in monthly_labels]
ax.set_xticks(corresponding_ticks)
ax.set_xticklabels(monthly_labels, rotation=90, fontsize=8)
plt.yticks(fontsize=8)
ax.set_ylim(bottom=0)
plt.ylabel('Volatility of log returns')
plt.xlabel('Date')
plt.tight_layout()
plt.savefig('plots/volatility_over_time.png', dpi=200)
plt.close()

print('\n' + str(len(df.index)) + ' datapoints')
