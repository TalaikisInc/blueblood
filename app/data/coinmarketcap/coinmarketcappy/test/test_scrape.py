import coinmarketcappy as cmc
import time
import datetime


temp = cmc.get_ticker_historical(name='bitcoin', out_file='test', wformat='csv', epoch=True)
print(temp)
time.sleep(6)

temp = cmc.available_snaps('test1', 'csv')
print(temp)
time.sleep(6)

temp = cmc.historical_snapshots(['20180401', '20180408'],
                                'test2.csv',
                                # 'historical_snaps.json',
                                rformat='json', wformat='csv')
for x in temp:
    print(x)
    for y in temp[x]:
        print(y)
time.sleep(6)

dominance = cmc.dominance(out_file='test3', wformat='csv', formatted='raw', epoch=False)
for x in dominance:
    print(x, dominance[x])
time.sleep(6)

dominance = cmc.dominance(start=datetime.datetime(2018, 4, 3, 2, 40, 1), end='2018-05-01-16-02-03',
                          out_file='test3', wformat='csv', formatted='alt', epoch=False)
for x in dominance:
    print(x, dominance[x])
time.sleep(6)

total_mc = cmc.total_market_cap(exclude_btc=False, epoch=False, out_file='test4', wformat='csv')
print(total_mc)
time.sleep(6)

total_mc = cmc.total_market_cap(exclude_btc=True, epoch=True)
print(total_mc)

# print(list(dominance['bitcoin'].keys()))
# print(list(dominance['bitcoin'].values()))
# print(list(dominance['altcoins'].values()))
