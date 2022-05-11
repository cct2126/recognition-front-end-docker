import json

import redis

r = redis.Redis(host='112.74.161.101', port=32003, db=0)
print(r.keys())
# for elem in r.keys():
#     r.delete(elem)
# print(r.keys())
temp = r.keys()
for elem in temp:

    tmp = (r.get(elem)).decode('utf-8')

    label = tmp.split("=")[1].split(";")[0]
    data = tmp.split("object=")[1]

    print(label)
    print(data.encode('utf-8'))



    # tmp = json.loads(tmp)
    # print(tmp)
    # print(tmp['result'])


