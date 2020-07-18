# excel的格式为
# [0] 剩余参数行，用于存放新增需求类型。此时只有(0,0)单元格用到，记录键值数量。
# [1] 导出到目标。值为"s","c"或"sc"，s表示该键值导出到服务端，c表示该键值导出到客户端
# [2] 数据类型。目前有四种类型，数值，字符串，一维数组和二维数组。一维数组用self.arrType表示，
#     二维数组分别由self.twoArrTypeKey和self.twoArrTypeValue组成一个数组值，存放到以该键名定义的数组中。
# [3] 键名。当该键作为主键时无用，因为主键用单元格值为键。
# [4] 键的一些描述
# [5] 从该行开始就是正式的数据。
# ...

# 实例
# [0] 1
# [1] sc       c      sc   sc    sc     sc    c     c      c       c
# [2] int    string   int int    array  array a     b      a       b
# [3] heroid name     hp  attack skill skill reward reward reward reward
# [4] 英雄id 英雄名称 血量 攻击力 技能组 技能组 奖励   奖励    奖励   奖励
# [5] 1001   雷神     110   12   1001        2001   10     2005    31
# 【6】 1002   巨猿     120   11          1002               2002    50

# 上述的数组中位置可以随意填，只要键名一样即可。而二位数组需要保持ab成对出现。


import xlrd
import os
import json


class DaoCfg(object):
    def __init__(self):
        super(DaoCfg, self).__init__()
        self.init()

    def init(self):
        self.oriDir             = "D:/wsx/py/server/xls/"              # 源文件夹
        self.tarClientDir       = "D:/wsx/py/server/config/client/"    # 客户端的目标文件夹
        self.tarServerDir       = "D:/wsx/py/server/config/server/"    # 服务端的目标文件夹
        self.supportType        = [".xls"]                             # 只处理源文件夹中支持的格式类型的文件
        self.tarFileType        = ".json"                              # 目标文件后缀

        self.keyNum             = [0,0]                                # 键的数量（单元格坐标）
        self.realyLine          = 5                                    # 从这行开始才是真正的数据
        self.intType            = "int"                                # 以下为定义单元格数据类型
        self.strType            = "string"
        self.arrType            = "array"
        self.twoArrTypeKey      = "a"
        self.twoArrTypeValue    = "b"

        self.scLine             = 1                                    # 定义导出为客户端/服务端类型的行(从0开始)
        self.typeLine           = 2                                    # 定义单元格数据类型的行(从0开始)
        self.keyLine            = 3                                    # 定义键值的行(从0开始)

        self.cellTypeEmpty      = 0                                    # 以下为单元格数据的类型
        self.cellTypeString     = 1
        self.cellTypeNumber     = 2
        self.cellTypeBoolean    = 4

    def destroy(self):
        pass

    def start(self):
        filePath     = ""
        oriFileArray = os.listdir(self.oriDir)
        for file in oriFileArray:
            filePath = self.oriDir + file
            if self.isFileSupport(filePath) is True:
                self.openExcel(filePath)
    
    def openExcel(self, filePath):
        excel          = xlrd.open_workbook(filePath)
        sheetNameArray = excel.sheet_names()
        sheet          = None
        for sheetName in sheetNameArray:                               # 遍历每个sheet
            sheet = excel.sheet_by_name(sheetName)
            self.packJson(sheet)

    def packJson(self, sheet):
        clientJson = {}
        serverJson = {}
        keyNum     = int(sheet.cell(self.keyNum[0], self.keyNum[1]).value)

        for col, colValue in enumerate(sheet.col_values(0)):           # 行
            tarObjClient = clientJson
            tarObjServer = serverJson
            for row, rowValue in enumerate(sheet.row_values(0)):       # 列
                if col < self.realyLine:
                    break
                if row < keyNum:                                       # key
                    key = self.getValue(sheet, col, row)
                    if tarObjClient.get(key) == None:
                        tarObjClient[key] = {}
                        tarObjServer[key] = {}
                    tarObjClient = tarObjClient[key]
                    tarObjServer = tarObjServer[key]
                else:                                                  # value
                    key   = self.getKey(sheet,self.keyLine,row)
                    value = self.getValue(sheet,col,row)
                    vType = self.getKey(sheet,self.typeLine,row)
                    sc    = self.getKey(sheet,self.scLine,row)
                    scArr = [self.isDaoClient(sc),self.isDaoServer(sc)]
                    ############################################################################
                    # 以下为不同单元格类型的处理方式，新增类型则在下面添加新判断即可
                    if vType == self.intType:
                        if scArr[0] is True:
                            tarObjClient[key] = value
                        if scArr[1] is True:
                            tarObjServer[key] = value

                    elif vType == self.strType:
                        if scArr[0] is True:
                            tarObjClient[key] = value
                        if scArr[1] is True:
                            tarObjServer[key] = value

                    elif vType == self.arrType:
                        if scArr[0] is True:
                            if tarObjClient.get(key) == None:
                                tarObjClient[key] = []
                            if value != "":
                                tarObjClient[key].append(value)
                        if scArr[1] is True:
                            if tarObjServer.get(key) == None:
                                tarObjServer[key] = []
                            if value != "":
                                tarObjServer[key].append(value)

                    elif vType == self.twoArrTypeKey:
                        if scArr[0] is True:
                            if tarObjClient.get(key) == None:
                                tarObjClient[key] = []
                            if value != "":
                                newCArray = []
                                newCArray.append(value)
                                tarObjClient[key].append(newCArray)

                        if scArr[1] is True:
                            if tarObjServer.get(key) == None:
                                tarObjServer[key] = []
                            if value != "":
                                newSArray = []
                                newSArray.append(value)
                                tarObjServer[key].append(newSArray)

                    elif vType == self.twoArrTypeValue:
                        if scArr[0] is True and len(tarObjClient[key]) > 0:
                            tarArray = tarObjClient[key][len(tarObjClient[key]) - 1]
                            tarArray.append(value)
                        if scArr[1] is True and len(tarObjServer[key]) > 0:
                            tarSArray = tarObjServer[key][len(tarObjServer[key]) - 1]
                            tarSArray.append(value)

        # print(json.dumps(clientJson,indent=1))
        # print(json.dumps(serverJson,indent=1))
        self.write2JSON(sheet, clientJson, serverJson)

    def write2JSON(self, sheet, clientJson, serverJson):
        tarClientFile = self.tarClientDir + sheet.name + self.tarFileType
        tarServerFile = self.tarServerDir + sheet.name + self.tarFileType

        jsonFile = open(tarClientFile, "w",)
        jsonFile.write(json.dumps(clientJson, indent=4))  # indent=4 缩进处理
        jsonFile.close()

        jsonFile = open(tarServerFile, "w",)
        jsonFile.write(json.dumps(serverJson, indent=4))
        jsonFile.close()
        print("写入 " + sheet.name + " 完成")

    def removeAllFile(self):
        cDir = os.listdir(self.tarClientDir)
        sDir = os.listdir(self.tarServerDir)

        filePath = ""
        for file in cDir:
            filePath = self.tarClientDir + file
            os.remove(filePath)
        for file in sDir:
            filePath = self.tarServerDir + file
            os.remove(filePath)
        
    # ---------------------------------------------------------------------- Tools
    # 判断该文件是否为支持文件
    def isFileSupport(self, filePath):
        fileType = os.path.splitext(filePath)[1]
        for sType in self.supportType:
            if sType == fileType:
                return True
        return False

    def getValue(self, sheet, col, row):
        vType = sheet.cell(self.typeLine,row).value
        value = sheet.cell(col, row).value
        if vType == self.intType and value != "":
            return int(value)
        if vType == self.arrType or vType == self.twoArrTypeValue:
            t = sheet.cell_type(col, row)
            if t == self.cellTypeNumber:
                return int(value)
        return value

    def getKey(self, sheet, col, row):
        value = sheet.cell(col, row).value
        return value

    # 判断是否为到客户端类型
    def isDaoClient(self, daoType: str):
        return daoType.find("c") >= 0

    # 判断是否为到服务端类型
    def isDaoServer(self, daoType: str):
        return daoType.find("s") >= 0


D = DaoCfg()
D.removeAllFile()
D.start()
D.destroy()


# xlrd
# open_workbook(filePath)        返回一个excel对象
# excel.sheet_names()            返回excel里的页签名称数组
# excel.sheet_by_name(sheetName) 通过页签名称打开页签内容，返回一个sheet对象
# sheet.cell(x,y)                返回单元格，但不是值，值在.value中。
# sheet.cell_type(e,y)           返回单元格值的类型



