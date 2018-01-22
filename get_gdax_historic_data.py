import requests
import datetime as dt
import time

product_id = 'BTC-USD'
uri = 'https://api.gdax.com/products/' + product_id + '/candles'

start = dt.datetime(2016, 1, 1, 0, tzinfo=dt.timezone.utc)
end   = dt.datetime(2018, 1,20,23, tzinfo=dt.timezone.utc)
delta = dt.timedelta(hours=300) # 5 hrs if gran=60, 75 if gran=900, 300 if gran=3600
granularity = 3600 # seconds

data = []
slice_start = start
while slice_start < end:
    print(slice_start)
    slice_end = slice_start + delta
    response = requests.get(uri, {'start':       slice_start.isoformat(),
                                  'end':         slice_end.isoformat(),
                                  'granularity': granularity})
    while response.status_code == 429:
        print('sleeping 5 seconds')
        time.sleep(5)
        response = requests.get(uri, {'start':       slice_start.isoformat(),
                                      'end':         slice_end.isoformat(),
                                      'granularity': granularity})
    if response.status_code != 200 and response.status_code != 429:
        print(response)
        print(response.json())
        quit()
    
    data += response.json()
    slice_start = slice_end
    time.sleep(0.5)

data.sort(key=lambda x: x[0])

# Dedupe by timestamp.
len_before_dedupe = len(data)
for i in reversed(range(len(data)-1)):
    if data[i][0] == data[i+1][0]:
        del data[i+1]
print("Removed " + str(len_before_dedupe - len(data)) + " duplicates.")

filename = ('gdax_' + product_id.lower() + '_candles_gran'
            + str(granularity) + '_' + start.strftime('%Y%m%d%H') + '-'
            + slice_start.strftime('%Y%m%d%H') +'.csv')
with open(filename,'w') as fp:
    fp.write('time,low,high,open,close,volume\n')
    for row in data:
        fp.write(','.join([str(x) for x in row]) + '\n')
