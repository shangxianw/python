import json
import csv

tarPath = "./config/ok.csv"
dataPath = "./data/"
cfgPath = "./config/money2.json"
MONEY = json.loads(open(cfgPath, "r", encoding="utf-8").read())
moneyInfo = {}  # key[] 0date 1open 2high 3low 4close
gapInfo = {}    # key{} data:number
okInfo = []


def initInfo():
    title = ["date"]
    okInfo.append(title)

    for key in MONEY:
        moneyInfo[key] = []
        csvPath = dataPath + MONEY[key]["fileName"]
        file = open(csvPath, "r", encoding="utf-8")
        csvInfo = csv.reader(file)
        for item in csvInfo:
            newItem = []
            newItem.append(item[0])
            newItem.append(float(item[2]))
            newItem.append(float(item[3]))
            newItem.append(float(item[4]))
            newItem.append(float(item[5]))
            moneyInfo[key].insert(0, newItem)

            date = [item[0]]
            okInfo.append(date)

        m1 = key[0:3]
        m2 = key[3:6]
        gapInfo[m1] = {}
        gapInfo[m2] = {}


def calcGap():
    for key in moneyInfo:
        for item in moneyInfo[key]:
            m1 = key[0:3]
            m2 = key[3:6]
            point = MONEY[key]["point"]
            gap = int((item[4] - item[1]) / point)
            # print(item[4], item[1], gap)
            try:
                gapInfo[m1][item[0]] += gap
            except BaseException:
                gapInfo[m1][item[0]] = 0
                gapInfo[m1][item[0]] += gap
            try:
                gapInfo[m2][item[0]] += gap
            except BaseException:
                gapInfo[m2][item[0]] = 0
                gapInfo[m2][item[0]] += gap * -1
        #     break
        # break


def WriteToCsv():
    csvfile = open(tarPath, 'w', newline='')
    writer = csv.writer(csvfile)
    for money in gapInfo:
        okInfo[0].append(money)
    # for
    writer.writerows(okInfo)
    csvfile.close()
    pass


initInfo()
calcGap()
WriteToCsv()
print(okInfo)

for key in gapInfo:
    for date in gapInfo[key]:
        print(key, date, gapInfo[key][date])
#     print("----------------------------------")
# gapInfo
# {
#     "usd": {
#         "2019.11.19": 500,
#         "2019.11.18": -290,
#     },
#     "eur": {
#         "2019.11.19": 500,
#         "2019.11.18": -290,
#     },
# }
