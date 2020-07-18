# 数据源为csv文件，内容格式为 0date 1time 2open 3high 4low 5close 6volume
# 需要判断数据源的有效性，排除有些货币对无对应日期数据的情况。
# 需要制作出的数据有:
#	1、各货币每日相对其他货币的涨跌幅
#	2、涨货币与跌货币的总和(计算出总资金是否有流入或流出)

import json
import csv

class DoData(object):
	def __init__(self):
		super(DoData, self).__init__()
		self.init()

	def init(self):
		pass
		self.mCfg = "./config/crossMoney.json"
		self.oriDataPath = "./data/"
		self.date = "2019.11.22"

		self.cfgJson = None
		self.oriMap = {}
		self.gapMap = {}

	def destroy(self):
		self.oriMap = None
		pass

	def start(self):
		mCfgFile = open(self.mCfg, "r", encoding="utf-8")
		mCfgTxt = mCfgFile.read()
		self.cfgJson = json.loads(mCfgTxt)
		# print(self.cfgJson)
		mCfgFile.close()
		for money in self.cfgJson:
			self.oriMap[money] = {}
			m1 = money[0:3]
			m2 = money[3:6]
			if self.gapMap.get(m1) == None:
				self.gapMap[m1] = 0
			if self.gapMap.get(m2) == None:
				self.gapMap[m2] = 0


			oriFilePath = self.oriDataPath + self.cfgJson[money]["fileName"]
			# print(oriFilePath)
			csvFile = open(oriFilePath, "r", encoding="utf-8")
			reader  = csv.reader(csvFile)
			for item in reader:
				date     = item[0]
				if date == self.date:
					dateInfo = [None] * 4
					dateInfo[0] = float(item[2])
					dateInfo[1] = float(item[3])
					dateInfo[2] = float(item[4])
					dateInfo[3] = float(item[5])
					self.oriMap[money][date] = dateInfo
		self.calcGap()

	def calcGap(self):
		for money in self.oriMap:
			priceInfo = self.oriMap[money][self.date]
			oPrice = priceInfo[0]
			oClose = priceInfo[3]
			point  = self.cfgJson[money]["point"]
			gap = round((oClose - oPrice)/point)
			m1 = money[0:3]
			m2 = money[3:6]
			self.gapMap[m1] += gap
			self.gapMap[m2] += gap * -1


D = DoData()
D.start()
# for i in D.oriMap:
# 	print(D.oriMap[i])
print(D.gapMap)