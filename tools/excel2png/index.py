import sys
import os
import json
from win32com.client import Dispatch, DispatchEx
import pythoncom
from PIL import ImageGrab, Image
import uuid
import wui
import xlrd

class Index:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.configDir = "C:\\Users\\User\\AppData\\Excel2Png\\"
        self.configFile = "config.json"
        self.configJson = None
        self.SaveKey = "saveDir"
        self.OriKey  = "oriDir"

        self.excel = None
        self.wb = None
    
    def start(self):
        self.win = wui.Panel()
        self.win.setTitle("excel内容存为图片")
        self.win.setSize(400, 170)
        self.win.resizable(False, False)
        self.initView()
        self.initData()
        self.win.mainloop()
    
    def initView(self):
        self.btn1 = wui.Button(self.win)
        self.btn1.x = 10
        self.btn1.y = 10
        self.btn1.label = "点我选择文件"

        self.lb1 = wui.Label(self.win)
        self.lb1.x = 100
        self.lb1.y = 13
        self.lb1.text2 = "文件地址"

        self.btn2 = wui.Button(self.win)
        self.btn2.x = 10
        self.btn2.y = 50
        self.btn2.label = "选择保存位置"

        self.lb2 = wui.Label(self.win)
        self.lb2.x = 100
        self.lb2.y = 53
        self.lb2.text2 = "保存地址"

        self.saveBtn = wui.Button(self.win)
        self.saveBtn.x = 10
        self.saveBtn.y = 90
        self.saveBtn.label = "点我转为图片"

        self.lb3 = wui.Label(self.win)
        self.lb3.x = 10
        self.lb3.y = 130
        self.lb3.text2 = "注意事项：1、截图的宽度至少到AA单元格位置，因为api的关系\n识别不了图片的有效位置"
    
    def initData(self):
        path = self.getConfig()
        with open(path, "r", encoding="utf-8") as f:
            self.configJson = json.load(f)
        
        self.lb1.text2 = self.configJson[self.OriKey]
        self.lb2.text2 = self.configJson[self.SaveKey]
        self.btn1.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnBtn1Tap)
        self.btn2.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnBtn2Tap)
        self.saveBtn.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnSaveTap)
    
    ## ---------------------------------------------------------------------- excel
    def openExcel(self, path:str):
        self.excel = DispatchEx("Excel.Application")
        self.excel.Visible = False
        self.excel.DisplayAlerts = False
        self.wb = self.excel.Workbooks.Open(path)
    
    ## ---------------------------------------------------------------------- 处理sheet并保存为图片
    def doSheet(self, excelName:str, sheetName:str, area:str):
        saveName = self.lb2.text2 + "/" + excelName + "_" + sheetName + ".png"
        try:
            ws = self.wb.Sheets(sheetName)
            ws.Activate()
            ws.Range(area).CopyPicture()
            ws.Paste()
            self.excel.Selection.ShapeRange.Name = sheetName
            ws.Shapes(sheetName).Copy()
            img = ImageGrab.grabclipboard()

            img.save(saveName)
            print(saveName + " success!")
        except(BaseException):
            print(saveName + " error!")

    ## ---------------------------------------------------------------------- 关闭当前excel
    def closeExcel(self):
        self.wb.Close()
        self.excel.Quit()
    
    def recordSheet(self, path:str):
        b = xlrd.open_workbook(path)
        sheetArray = []
        for sheet in b.sheets():
            sheetArray.append([sheet.name, sheet.nrows, sheet.ncols])
        return sheetArray
    
    def killWps(self):
        os.system("taskkill /f /im wps.exe")
        os.system("taskkill /f /im et.exe")
    
    def getArea(self, ncols:int, nrows:int):
        try:
            arr = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 
                    "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH"]
            x = "AA"
            index = arr.index(x)
            if ncols > index:
                x = arr[index]
            return "A1:" + x + str(nrows+20)
        except(BaseException):
            return "A1:AA150" # 固定宽为AA是因为图片是不占单元格的，会导致读取的有效列数不够。
    
    def updateConfig(self):
        self.configJson[self.OriKey] = self.lb1.text2
        self.configJson[self.SaveKey] = self.lb2.text2
        path = self.getConfig()
        with open(path, "w", encoding="utf-8") as f:
            content = json.dumps(self.configJson)
            f.write(content)
        
    def checkValid(self):
        if os.path.isfile(self.lb1.text2) is False:
            wui.alert("error", "目标文件不是一个文件")
            return False
        
        if os.path.splitext(os.path.basename(self.lb1.text2))[1] != ".xlsx": 
            wui.alert("error", "请选择excel文件")
            return False
        
        if os.path.isdir(self.lb2.text2) is False:
            wui.alert("error", "目标地址不是一个文件夹")
            return False
    
    def getConfig(self):
        if os.path.exists(self.configDir) is False:
            os.mkdir(self.configDir)
        path = self.configDir + self.configFile
        if os.path.exists(path) is False:
            with open(path, "w", encoding="utf-8") as f:
                content = '{"saveDir": "C:/Users/User/Desktop", "oriDir": "./"}'
                f.write(content)
        return path

    ## ---------------------------------------------------------------------- Event
    ## ---------------------------------------------------------------------- Event
    def OnBtn1Tap(self, e):
        path = wui.openFileDialog()
        self.lb1.text2 = path
    
    def OnBtn2Tap(self, e):
        dir = wui.openDirDialog()
        self.lb2.text2 = dir
    
    def OnSaveTap(self, e):
        if self.checkValid() is False:
            return
        
        self.updateConfig()
        self.killWps()
        path = self.lb1.text2
        excelName = os.path.splitext(os.path.basename(path))[0]
        self.openExcel(path)
        sheetArray = self.recordSheet(path)
        for sheetInfo in sheetArray:
            sheetName = sheetInfo[0]
            nrows     = sheetInfo[1] + 20
            ncols     = sheetInfo[2] + 1
            area      = self.getArea(ncols, nrows)
            self.doSheet(excelName, sheetName, area)
        self.closeExcel()
        self.killWps()
        wui.alert("ok", "okk!")

if __name__ == "__main__":
    d = Index()
    d.start()