import redis
import random
import string

pool = redis.ConnectionPool(host="localhost", port=6379, db=1, password="123456");
r = redis.Redis(connection_pool=pool);
sKey = "student.score";

def createStudent():
    r.delete(sKey);
    for i in range(10):
        score = round((random.random() * 100), 2);
        studentName = "".join(random.sample(string.ascii_letters, 6));
        r.zadd(sKey, {studentName : score});
    

createStudent();

# 随机获取一个学生的信息
name, score = r.zrevrange(sKey, 0, 9, withscores=True)[random.randint(0, 10)];
print(name, ":" ,score);

# 获取0-50分数阶段的学生数量
count = r.zcount(sKey, 0 , 50);
print("学生数量:", count);

print('{}:{}'.format("学生", "分数"));
for name, score in r.zrevrangebyscore(sKey, 100, 0, start=0, num=3, withscores=True):
    print(name, ":", score);
