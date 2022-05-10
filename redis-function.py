import redis

r = redis.Redis(host='112.74.161.101', port=32003, db=0)
print(r.keys())
# for elem in r.keys():
#     r.delete(elem)
# print(r.keys())
temp = r.keys()
for elem in temp:
    r.get(elem)
    print("emm")
