import re
import sys
import json

timezone = {
    "Beijing": +8,
    "Tokyo": +9,
    "Bangkok": +7,
    "Ottawa": -5,
    "Los Angeles": -8,
    "Alaska": -9,
    "Sydney": +10,
    "Suva": +12,
    "Oakland": +12,
    "Moscow": +3,
    "Stockholm": +1,
    "Geneva": +1,
    "Cape Town": +2,
    "Khartoum": +3,
    "Lima": -5,
    "Rio de Janeiro": -3,
    "Santiago": -8
}


def is_same_sign(depart, dest):
    """
    东加西减: 已知东时区求西时区加，否者减
    同加异减: 在同一时区加，否者减
    """
    if (depart > 0 and dest > 0) or (depart < 0 and dest < 0):
        return True
    elif dest < 0 and depart > 0:
        return True
    elif dest > 0 and depart < 0:
        return False
    else:
        return False


def get_append_day(s):
    m = re.findall('.*\+(\d).*', s)
    if len(m) > 0:
        return int(m[0])
    else:
        return 0


def parse2time24(s):
    arr = s.split()
    if not s:
        return
    if arr[1] == 'am':
        t = arr[0].split(':')
        rt = int(t[0]) * 60 + int(t[1]) if len(t) == 2 else 0
    elif arr[1] == 'pm':
        t = arr[0].split(':')
        rt = (int(t[0]) + 12) * 60 + int(t[1]) if len(t) == 2 else 0
    else:
        rt = 0
    return rt

min_time_data = dict()
min_money_data = dict()


with open('data/data.json', 'r') as f:
    data = json.load(f)
    for k, v in data.items():
        citys = k.split('->')
        depart = citys[0]
        dest = citys[1]
        prices, sptimes = [], []
        for item in v:
            depart_time = parse2time24(item['depart_time'])
            arrive_time =  parse2time24(item['arrive_time'])
            if not depart_time or not arrive_time:
                continue
            price = item['price'].replace('$', '')
            spend_time = abs(arrive_time - depart_time)
            flag = 1 if is_same_sign(timezone[depart], timezone[dest]) else -1
            time_lag = abs(timezone[depart] - timezone[dest]) * 60 * flag
            if arrive_time < depart_time:
                spend_time = 24 * 60 - spend_time
            append_day = get_append_day(item['arrive_time'])
            rt = 24 * append_day * 60 + time_lag + spend_time
            prices.append(price)
            sptimes.append(rt)
            # print(depart, dest, rt, price)
        sptimes = [s for s in sptimes if s > 0]
        if len(prices) == 0 or len(sptimes) == 0:
            mp = sys.maxsize
            mt = sys.maxsize
        else:
            mp = min(prices)
            mt = min(sptimes)
        if depart not in min_time_data:
            min_time_data[depart] = {
                dest: mt
            }
        else:
            min_time_data[depart][dest] = mt
        
        if depart not in min_money_data:
            min_money_data[depart] = {
                dest: mp
            }
        else:
            min_money_data[depart][dest] = mp
        
citys = ['Beijing', 'Tokyo', 'Bangkok', 'Ottawa', 'Los Angeles', 'Alaska', 'Sydney', 'Suva', 'Oakland', 'Moscow', 'Stockholm', 'Geneva', 'Cape Town', 'Khartoum', 'Lima', 'Rio de Janeiro', 'Santiago']
n = len(citys)
tt, mm = [], []
for i in range(n):
    t, m = [], []
    for j in range(n):
        if i != j:
            t.append(min_time_data[citys[i]][citys[j]])
            m.append(min_money_data[citys[i]][citys[j]])
        else:
            t.append(0)
            m.append(0)
    tt.append(t)
    mm.append(m)
