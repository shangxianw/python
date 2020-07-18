import csv
import json

cfgPath = "./config/money.json"
dataDir = "./data/"

MONEY = json.loads(open(cfgPath,"r",encoding="utf-8").read())
date = "2008.04.22";

# 0date  1time  2open  3high 4low 5close 6volume
# 7money 8hlGap 9upGap 8downGap
dayData = {}


def initData():
	for key in MONEY:
		mFile     = dataDir + MONEY[key]["fileName"]
		point     = MONEY[key]["point"]
		file      = open(mFile,"r",newline="")

		reader = csv.reader(file)
		for item in reader:
			if item[0] == date:
				dayData[key] = []
				array        = dayData[key]
				array.append(item[0])
				array.append(item[1])
				array.append(float(item[2]))
				array.append(float(item[3]))
				array.append(float(item[4]))
				array.append(float(item[5]))
				array.append(int(item[6]))
				array.append(key)
				
				# 计算实体长度
				tmpGap       = array[5] - array[2]
				gap          = int(tmpGap / point)
				dayData[key].append(gap)

				# 计算上下影线
				if array[2] <= array[5]: # 阳线
					tmpUpGap   = array[3] - array[5]
					tmpDownGap = array[2] - array[4]
				else:
					tmpUpGap   = array[3] - array[2]
					tmpDownGap = array[5] - array[4]
				
				upGap   = int(tmpUpGap   / point)
				downGap = int(tmpDownGap / point)
				array.append(upGap)
				array.append(downGap)
				
		file.close()

def sortByOpenClose():
	pass

initData()
sortByOpenClose()
for key in dayData:
	print(dayData[key])