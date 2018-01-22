import requests
import datetime as dt
import time

cryptocoin = 'BTC'
uri = ('https://min-api.cryptocompare.com/data/histohour?fsym='
       + cryptocoin
       + '&tsym=KRW&limit=2000&aggregate=1&e=Korbit&toTs=')

start = dt.datetime(2016, 4,25,20, tzinfo=dt.timezone.utc)
end   = dt.datetime(2018, 1,20,23, tzinfo=dt.timezone.utc)
delta = dt.timedelta(hours=2000)

data = []
slice_end = start
while slice_end < end:
    slice_end += delta
    slice_end = min(slice_end, end)
    print(slice_end)
    response = requests.get(uri + str(int(slice_end.timestamp())))

    if response.status_code != 200:
        print(response)
        print(response.json())
        quit()
    
    # Reformat data from json to list.
    for xs in response.json()['Data']:
        row = [xs['time'], xs['low'], xs['high'], xs['open'], xs['close'],
               xs['volumefrom'], xs['volumeto']]
        data.append(row)

data.sort(key=lambda x: x[0])

# Dedupe by timestamp.
len_before_dedupe = len(data)
for i in reversed(range(len(data)-1)):
    if data[i][0] == data[i+1][0]:
        del data[i+1]
print("Removed " + str(len_before_dedupe - len(data)) + " duplicates.")

# Dedupe by timestamp.
#data = [list(t) for t in {tuple(row) for row in data}] # dedupe
for i in reversed(range(len(data)-1)):
    if data[i][0] == data[i+1][0]:
        del data[i+1]
print(len(data))

filename = ('korbit_' + cryptocoin.lower() + '-krw_candles_gran3600_'
            + start.strftime('%Y%m%d%H') + '-'
            + slice_end.strftime('%Y%m%d%H') +'.csv')
with open(filename,'w') as fp:
    fp.write('time,low,high,open,close,volumefrom,volumeto\n')
    for row in data:
        fp.write(','.join([str(x) for x in row]) + '\n')
