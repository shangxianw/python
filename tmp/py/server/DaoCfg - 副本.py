import xlrd
import os
import json


class DaoCfg(object):

    def __init__(self):
        super(DaoCfg, self).__init__()
        self.init()

    def init(self):
        self.oriDir       = "D:/wsx/py/server/xls/"              # 源文件夹
        self.tarClientDir = "D:/wsx/py/server/config/client/"    # 目标文件夹
        self.tarServerDir = "D:/wsx/py/server/config/server/"    # 目标文件夹
        self.supportType  = [".xls"]                             # 只处理源文件夹中支持的格式类型的文件

        self.keyNum             = [0,0] # 键的数量
        self.realyLine          = 5  # 从这行开始才是真正的数据
        self.intType            = "int"
        self.strType            = "string"
        self.arrType            = "array"
        self.doubleArrTypeKey   = "a"
        self.doubleArrTypeValue = "b"

        self.keyLine             = 3

    def destroy(self):
        self.oriDir = None
        self.tarDir = None
        self.supportType = None

    def start(self):
        filePath = ""

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
        # serverJson = {}
        keyNum     = int(sheet.cell(self.keyNum[0], self.keyNum[1]).value)
        # keyArray   = [None] * keyNum

        for col, colValue in enumerate(sheet.col_values(0)):           # 行
            tarObjClient = clientJson
            # tarObjServer = serverJson
            for row, rowValue in enumerate(sheet.row_values(0)):       # 列
                if col < self.realyLine:
                    break
                if row < keyNum:                                       # key
                    key = self.getValue(sheet, col, row)
                    if tarObjClient.get(key) == None:
                        tarObjClient[key] = {}
                        # tarObjServer[key] = {}
                    tarObjClient = tarObjClient[key]
                    # tarObjServer = tarObjServer[key]
                else:
                    key = self.getValue(sheet,self.keyLine,row)
                    value = self.getValue(sheet,col,row)
                    tarObjClient[key] = value



        # for col, colValue in enumerate(sheet.col_values(0)):           # 行
        #     for row, rowValue in enumerate(sheet.row_values(0)):       # 列
        #         if col < self.realyLine:
        #             break
        #         if row == 0:                                            # 初始化key结构
        #             tarObjClient = clientJson
        #             tarObjServer = serverJson
        #             for index in range(keyNum):
        #                 value = self.getValue(sheet, col, index)
        #                 if value != "":
        #                     keyArray[index] = value
        #                     tarObjClient[value] = {}
        #                     tarObjServer[value] = {}
        #                 tarObjClient = tarObjClient[keyArray[index]]
        #                 tarObjServer = tarObjServer[keyArray[index]]

                # if self.isDaoClient(self.getValue(sheet, 1, row)):
                #     self.fixData(sheet, clientJson, keyArray, col, row)

                # if self.isDaoServer(self.getValue(sheet, 1, row)):
                #     self.fixData(sheet, serverJson, keyArray, col, row)

        print(json.dumps(clientJson,indent=1))
        # print(json.dumps(serverJson,indent=1))
        # tarClientFile = self.tarClientDir + sheet.name + ".json"
        # tarServerFile = self.tarServerDir + sheet.name + ".json"

        # jsonFile = open(tarClientFile, "w",)
        # jsonFile.write(json.dumps(clientJson, indent=1))  # indent=1 格式化处理
        # jsonFile.close()

        # jsonFile = open(tarServerFile, "w",)
        # jsonFile.write(json.dumps(serverJson, indent=1))
        # jsonFile.close()
        # print("写入 " + sheet.name + " 完成")

    # ?????????????????
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
    # 填充数据
    def fixData(self, sheet, tarObj, col, row):
        pass
        # for key in keyArray:
        #     tarObj = tarObj[key]

        #     key = self.getValue(sheet, 3, row)
        #     keyValue = self.getValue(sheet, col, row)
        #     if keyValue == "" or keyValue == None:
        #         return
        #     keyType = self.checkKeyType(sheet, row)
        #     if keyType == 1:  # 一般字段
        #         tarObj[key] = keyValue

        #     elif keyType == 2:  # 一维数组
        #         keyName = self.getValue(sheet, 3, row)
        #         try:
        #             tarObj[keyName].append(keyValue)
        #         except BaseException:
        #             tarObj[keyName] = []
        #             tarObj[keyName].append(keyValue)

        #     elif keyType == 3:  # 二维数组
        #         keyName = self.getValue(sheet, 3, row)
        #         try:
        #             if sheet.cell(2, row).value == "a":
        #                 newArray = []
        #                 newArray.append(keyValue)
        #                 tarObj[keyName].append(newArray)
        #             elif sheet.cell(2, row).value == "b":
        #                 l = len(tarObj[keyName])
        #                 tarObj[keyName][l - 1].append(keyValue)
        #         except BaseException:
        #             tarObj[keyName] = []
        #             newArray = []
        #             newArray.append(keyValue)
        #             tarObj[keyName].append(newArray)
    # ---------------------------------------------------------------------- Tools
    # 判断该文件是否为支持文件
    def isFileSupport(self, filePath):
        fileType = os.path.splitext(filePath)[1]
        for sType in self.supportType:
            if sType == fileType:
                return True
        return False

    def getValue(self, sheet, col, row):
        value = sheet.cell_type(col, row)
        if value == 2:
            return int(sheet.cell(col, row).value)
        return sheet.cell(col, row).value

    # 判断是否为到客户端类型
    def isDaoClient(self, daoType: str):
        for type in daoType:
            if type == "c":
                return True
        return False

    # 判断是否为到服务端类型
    def isDaoServer(self, daoType: str):
        for type in daoType:
            if type == "s":
                return True
        return False

    # 判断是否有分隔符
    def checkKeyType(self, sheet, row: int):
        type = sheet.cell(2, row).value
        if type == "arr":
            return 2
        elif type == "a" or type == "b":
            return 3
        return 1


D = DaoCfg()
D.removeAllFile()
D.start()
D.destroy()
