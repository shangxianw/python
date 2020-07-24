import os
import json
from win32com.client import Dispatch, DispatchEx
import pythoncom
from PIL import ImageGrab, Image
import uuid
import wui2 as wui
import xlrd
import demo



class SheetInfo:
    def __init__(self):
        self.sheetName = ""
        self.nrows = 0
        self.ncols = 0

class Index:
    def __init__(self):
        self.configPath = "D:\\wsx\\python\\tools\\excel2png\\data\\config.json"
        self.configData = None
        self.excelCfg = {}
        
        self.win = wui.Panel()
        self.win.setTitle("excel内容存为图片")
        self.win.setSize(400, 300)
        self.initView()
        self.initData()
        self.win.mainloop()
    
    def initView(self):
        self.lb1 = wui.Label(self.win)
        self.lb1.x = 10
        self.lb1.y = 10

        self.btn1 = wui.Button(self.win)
        self.btn1.x = 10
        self.btn1.y = 30
        self.btn1.label = "修改excel文件夹"

        self.lb2 = wui.Label(self.win)
        self.lb2.x = 10
        self.lb2.y = 60
        self.lb2.text2 = "此处为图片保存的文件夹"

        self.btn2 = wui.Button(self.win)
        self.btn2.x = 10
        self.btn2.y = 80
        self.btn2.label = "修改图片保存地址"

        self.saveBtn = wui.Button(self.win)
        self.saveBtn.x = 10
        self.saveBtn.y = 120
        self.saveBtn.label = "合成"
    
    def initData(self):
        with open(self.configPath, "r", encoding="utf-8") as f:
            self.configData = json.load(f)
            
        self.lb1.text2 = self.configData["oriDir"]
        self.lb2.text2 = self.configData["saveDir"]
        self.btn1.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnBtn1Tap)
        self.btn2.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnBtn2Tap)
        self.saveBtn.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnSaveTap)
    
    ## ---------------------------------------------------------------------- 开始
    def startChange(self):
        if os.path.isdir(self.configData["oriDir"]) is False or os.path.isdir(self.configData["saveDir"]) is False:
            wui.alert("error", "请选择正确的文件夹地址")
            return
        
        fileArray = os.listdir(self.configData["oriDir"])
        for file in fileArray:
            fileType = os.path.splitext(file)[1]
            if fileType != ".xlsx":
                continue
            path = self.configData["oriDir"] + "/" + file
            self.openSheet(path)
        self.compare()
    
    ## ---------------------------------------------------------------------- 记录
    def openSheet(self, path):
        b = xlrd.open_workbook(path)
        if b is None:
            return
        self.excelCfg[path] = []
        for sheet in b.sheets():
            item = SheetInfo()
            item.sheetName = sheet.name
            item.nrows = sheet.nrows
            item.ncols = sheet.ncols
            self.excelCfg[path].append(item)
    
    ## ---------------------------------------------------------------------- 合成
    def compare(self):
        for path in self.excelCfg:
            itemArray = self.excelCfg[path]
            for item in itemArray:
                excel_catch_screen(path, item.sheetName, "A1:J10")
    
    def writeJsonToFile(self):
        with open(self.configPath, "w", encoding="utf-8") as f:
            s = json.dumps(self.configData)
            f.write(s)

    def OnBtn1Tap(self, e):
        dir = wui.openDirDialog()
        self.lb1.text2 = dir
        self.configData["oriDir"] = dir
        self.writeJsonToFile()

    def OnBtn2Tap(self, e):
        dir = wui.openDirDialog()
        self.lb2.text2 = dir
        self.configData["saveDir"] = dir
        self.writeJsonToFile()
    
    def OnSaveTap(self, e):
        self.startChange()
        # excel_catch_screen("D:\\wsx\\python\\tools\\excel2png\\ss.xlsx", "争霸赛", "A1:x125")


if __name__ == "__main__":
    # d = Index()
    demo.excel_catch_screen("D:\\wsx\\python\\tools\\excel2png\\ss.xlsx", "争霸赛", "A1:x125")