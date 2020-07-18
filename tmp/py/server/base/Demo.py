import json
import os


# print(os.listdir("./config"))
print(1)
file = open("./config/shopdata.json","r",encoding='UTF-8')
content = json.load(file)
print(content["24010"]["desc"])
print(2)
# content = json.loads(file.read())
# print(content)