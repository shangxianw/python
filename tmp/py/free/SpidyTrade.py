import os
import requests
import json
import time

## ---------------------------------------------------------------------- Config
file = open("./config/money.json","r",encoding="utf-8")
text = file.read()
file.close()

MONEY    = json.loads(text)
saveDataPath = "./data/"
# print(MONEY["eurusd"]["sa"])
## ---------------------------------------------------------------------- Api
def reqData(moneyId:int):
	idStr   = str(moneyId)
	url     = 'https://tvc4.forexpros.com/8b299c39dd05ab72353f0c11840fae30/1574346592/6/6/28/history?symbol=' + idStr +'&resolution=D&from=1543243589&to=1574347649'
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3732.400 QQBrowser/10.5.3824.400"
	}
	strhtml = requests.get(url=url,timeout = 3000,headers=headers)
	return strhtml.text

def packTargetJsonData(moneyName,point,jsonData):
	tarJson          = {}
	tarJson["point"] = point
	tarJson["name"]  = moneyName
	tarJson["day"]   = []
	totalLen         = len(jsonData["t"])

	for index,value in enumerate(jsonData["t"]):
		obj = {}
		day = totalLen - index - 1
		sPoint = MONEY[moneyName]["savePoint"]

		obj["open"]  = round(jsonData["o"][day],sPoint)
		obj["close"] = round(jsonData["c"][day],sPoint)
		obj["high"]  = round(jsonData["h"][day],sPoint)
		obj["low"]   = round(jsonData["l"][day],sPoint)
		obj["time"]  = round(jsonData["t"][day],sPoint)
		
		tarJson["day"].append(obj)
	return tarJson

def writeToFile(tarJson,fileName):
	filePath = saveDataPath + fileName + ".json"
	tarFile  = open(filePath,"w",encoding="utf-8")
	tarData  = json.dumps(tarJson,indent=1)
	tarFile.write(tarData)
	tarFile.close()

## ---------------------------------------------------------------------- Edit
canStart = 1
for index,key in enumerate(MONEY):
	moneyName = key
	moneyId   = MONEY[key]["id"]
	point     = MONEY[key]["point"]
	
	if canStart == 0:
		break
	text     = reqData(moneyId)
	jsonData = packTargetJsonData(moneyName,point,json.loads(text))
	writeToFile(jsonData,moneyName)
	print(moneyName + "获取完成")
	time.sleep(3)
print("全部数据获取完成")

