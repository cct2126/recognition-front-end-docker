import json

import redis

r = redis.Redis(host='112.74.161.101', port=32003, db=0)
print(r.keys())
# for elem in r.keys():
#     r.delete(elem)
# print(r.keys())
img_keys = r.keys()
img_keys.sort(reverse=True)
img_keys = img_keys[:9]

for elem in img_keys:
    tmp = (r.get(elem)).decode('utf-8')
    label = tmp.split("=")[1].split(";")[0]
    data = tmp.split("object=")[1]
    print(label)



