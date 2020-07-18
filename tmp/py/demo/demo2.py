# redis应用场景
import redis
import random
import string

pool = redis.ConnectionPool(host="localhost", port=6379, db=0, password="123456");
r = redis.Redis(connection_pool=pool);


print(r.hgetall("1001")["name"]);
