import csv
import hashlib
 
m=hashlib.md5()
 
aaa=open('D:\\wsx\\python\\demo.csv', "wb")
csvwriter=csv.writer(aaa)
csvwriter.writerow(['created','md5'])
 
csvreader=open('D:\\wsx\\python\\demo.csv','r')
for line in csvreader:
    data=[]
    data.append(line.strip().split('|')[0])
    m.update(line.strip().split('|')[1])     #对分隔符的第二个字段加密
    encodeStr=m.hexdigest()
    data.append(encodeStr)
    data.append(line.strip().split('|')[2])
    csvwriter.writerow(data)