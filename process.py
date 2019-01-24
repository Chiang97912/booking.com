# -*- coding: utf-8 -*-
# @Author: Peter
# @Date:   2019-01-22 12:33:58
# @Last Modified by:   Peter
# @Last Modified time: 2019-01-24 16:33:06
import os
import json

result = dict()
count = 0
history = ''
for filename in os.listdir('data/'):
    with open(filename, 'r') as f:
        try:
            raw = f.read()
            data = json.loads(raw)
        except Exception as e:
            print('error:', f.read())
            continue
        for k, v in data.items():
            if k not in result and len(v) > 0:
                result[k] = v
                count += 1
                citys = k.split('->')
                history += '%s,%s\n' % (citys[0], citys[1])
with open('data/data.json', 'w') as f:
    f.write(json.dumps(result))
with open('history.csv', 'w') as f:
    f.write(history)
print(str(count))
