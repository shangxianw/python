import os

path = "./resource/config.txt"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
    input("exit")