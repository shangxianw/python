import sys
import os

#生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

path1 = resource_path("./resource/config.txt")
with open(path1, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
    input("exit")

path2 = "./config2.txt"
with open(path2, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
    input("exit")