import time
import json
import os
import sys
import wui
import whash
import tkinter as tk

class PropertyData:
    def __init__(self):
        self.propName = ""
        self.className = ""
        self.eventArray = []
    
    def packData(self, propName:str, className:str):
        self.propName = propName
        self.className = className
    
    def updateEventArray(self, array):
        self.eventArray = []
        for item in array:
            self.eventArray.append(item)
        print(self.eventArray)


class Demo:
    def __init__(self):
        workDir = os.getcwd()
        os.chdir(workDir)

        self.win = wui.Panel()
        self.win.setTitle("demo")
        self.win.setSize(1490, 620) # xuyao 需要居中显示
        self.win.resizable(False, False)
        self.initData()
        self.win.update(self.initView)
    
    def initData(self):
        self.propReplaceSign = "[property]"
        self.eventReplaceSign = "[event]"
        self.classReplaceSign = "[panelName]"

        self.saveDir = os.path.join(os.path.expanduser("~"), 'Desktop') + "/" # "C:\\Users\\User\\Desktop\\"
        self.exmlName = ""
        self.exmlPath = ""
        
        # 初始化事件
        self.eventPath = "D:\\wsx\\python\\tools\\exml2ts\\config\\event.json"
        self.eventJson = None
        self.eventNameArray = []
        with open(self.eventPath, "r", encoding="utf-8") as f:
            jsons = json.load(f)
            self.eventJson = jsons
            for key in jsons:
                self.eventNameArray.append(key)
        
        # self.templateDir = ".\\config\\template\\"
        self.templateDir = "D:\\wsx\\python\\tools\\exml2ts\\config\\template\\" # 为啥用相对不行
        self.templateFileArray = []
        self.currTemplateIndex = 0
        
        self.propMap = whash.WHash()

    def initView(self):
        self.menuBar = wui.Menu()
        self.menuBar.addCommand("设置")
        self.win.config(menu=self.menuBar)

        self.fileBtn = wui.Button(self.win)
        self.fileBtn.x = 10
        self.fileBtn.y = 10
        self.fileBtn.label = "打开文件"
        self.fileBtn.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnFileTap)

        self.listTit = wui.Label(self.win)
        self.listTit.text2 = "属性列表"
        self.listTit.x = 10
        self.listTit.y = 50

        # 左侧属性列表
        self.list = wui.SimpleList(self.win)
        self.list.x = 10
        self.list.y = 70
        self.list.width = 150
        self.list.height = 600
        self.list["exportselection"] = False
        self.list.addEventListener(wui.Event.ITEM_SELECT, self.OnPropListItemTap)
        wui.dragfiles(self.list, self.OnDragFile)

        self.nameTit = wui.Label(self.win)
        self.nameTit.text2 = "id名: "
        self.nameTit.x = 170
        self.nameTit.y = 10

        self.componentTit = wui.Label(self.win)
        self.componentTit.text2 = "组件: "
        self.componentTit.x = 170
        self.componentTit.y = 30

        self.name = wui.Label(self.win)
        self.name.text2 = "xxxxxxx"
        self.name.x = 210
        self.name.y = 10

        self.component = wui.Label(self.win)
        self.component.text2 = "xxxxxxx"
        self.component.x = 210
        self.component.y = 30

        self.eventListTit = wui.Label(self.win)
        self.eventListTit.text2 = "添加事件:"
        self.eventListTit.x = 170
        self.eventListTit.y = 50

        # 中间事件列表
        self.eventList = wui.SimpleList(self.win)
        self.eventList["selectmode"] = tk.MULTIPLE
        self.eventList.x = 170
        self.eventList.y = 70
        self.eventList.width = 300
        self.eventList.height = 200
        self.eventList.addEventListener(wui.Event.ITEM_SELECT, self.OnEventItemTap)

        # 右侧输入框
        self.area = wui.InputArea(self.win)
        self.area.x = 485
        self.area.y = 40
        self.area.width = 1000
        self.area.height = 570

        self.btn = wui.Button(self.win)
        self.btn.label = "生成ts模板"
        self.btn.x = 390
        self.btn.y = 10
        self.btn.width = 80
        self.btn.height = 35
        self.btn.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnOkBtn)

        self.templateTit = wui.Label(self.win)
        self.templateTit.text2 = "生成："
        self.templateTit.x = 480
        self.templateTit.y = 10
        
        # 右上侧单选模板
        varStr = tk.StringVar()
        varStr.set("template")
        self.templateFileArray = os.listdir(self.templateDir)
        index = 0
        for item in self.templateFileArray:
            tit = item + "模板"
            isSel = False
            radio = wui.RadioButton(self.win, text=tit, value=isSel, variable=varStr)
            radio.widgetName = str(index)
            radio.addEventListener(wui.TouchEvent.TOUCH_TAP, self.OnRadioClick)
            radio.place(x=520 + index * 130, y=10)
            index += 1
    
    ## ---------------------------------------------------------------------- 刷新左侧属性列表
    def updatePropShowInfo(self):
        if len(self.list.selectIndex) <= 0:
            print("当前未选中属性")
            return
        index = self.list.selectIndex[0]
        propName = self.list.dataProvider[index]
        propInfo = self.propMap.get(propName)
        self.name.text2 = propInfo.propName
        self.component.text2 = propInfo.className
    
    ## ---------------------------------------------------------------------- 刷新中间事件列表
    def updateEventList(self):
        if len(self.list.selectIndex) <= 0:
            print("当前未选中属性")
            return
        index = self.list.selectIndex[0]
        propName = self.list.dataProvider[index]
        propInfo = self.propMap.get(propName)

        self.eventList.dataProvider = self.eventNameArray
        self.eventList.selectIndex = propInfo.eventArray

    ## ---------------------------------------------------------------------- 刷新右侧模板内容
    def refreshTemplateContent(self):
        if len(self.list.selectIndex) <= 0:
            print("当前未选中属性")
            return
        fileName = self.templateFileArray[self.currTemplateIndex]
        path = self.templateDir + fileName
        with open(path, "r", encoding="utf-8") as f:
            tarContent = ""
            # 初始化原始内容
            content = f.read()
            tarContent = content.strip()
            # 替换类名
            tarContent = tarContent.replace(self.classReplaceSign, self.exmlName)
            # 替换属性
            propStr = ""
            for propInfo in self.propMap.values():
                tmpTemplate = "        private [propName]:[className];\n"
                tmpTemplate = tmpTemplate.replace("[propName]", propInfo.propName)
                tmpTemplate = tmpTemplate.replace("[className]", propInfo.className)
                propStr += tmpTemplate
            tarContent = tarContent.replace(self.propReplaceSign, propStr)
            # 替换事件
            eventStr = ""
            for propInfo in self.propMap.values():
                for eventIndex in propInfo.eventArray:
                    eventName = self.eventNameArray[eventIndex]
                    eventCfg = self.eventJson[eventName] # 获取到json里的数据

                    tmpTemplate = "            this.AddEvent(this.[propName], [eventName], this.[func], this);\n"
                    tmpTemplate = tmpTemplate.replace("[propName]", propInfo.propName)
                    tmpTemplate = tmpTemplate.replace("[eventName]", eventName)
                    tmpTemplate = tmpTemplate.replace("[func]", eventCfg["func"])
                    tmpTemplate = tmpTemplate.replace("[PropName]", propInfo.propName[0].title() + propInfo.propName[1:])
                    eventStr += tmpTemplate
            tarContent = tarContent.replace(self.eventReplaceSign, eventStr)
            self.area.text2 = tarContent

    def OnRadioClick(self, e):
        index = int(e.widget.widgetName)
        self.currTemplateIndex = index
        self.refreshTemplateContent()
    
    ## ---------------------------------------------------------------------- 重置数据和显示
    def resetDataAndView(self):
        self.propMap.destroy()
        self.list.dataProvider = []
        self.name.text2 = "xx"
        self.component.text2 = "xx"
        
        self.eventList.dataProvider = []
        self.area.text2 = ""


    ## ---------------------------------------------------------------------- 初始化属性列表
    def initPropList(self):
        self.resetDataAndView()
        with open(self.exmlPath, "r", encoding="utf-8") as f:
            contentArray = f.readlines()
            for content in contentArray:
                index = content.find(' id="')
                if index >= 0:
                    idStarIndex = index + 5
                    idEndIndex = content.find('"', idStarIndex)
                    ids = content[idStarIndex: idEndIndex]
                    
                    classStarIndex = content.find(':') + 1
                    classEndIndex  = content.find(' ', classStarIndex)
                    className = content[classStarIndex: classEndIndex]
                    print(ids + "  " + className)

                    propInfo = PropertyData()
                    propInfo.packData(ids, className)
                    self.propMap.set(ids, propInfo)
            self.list.dataProvider = self.propMap.keys()
            self.exmlName = os.path.splitext(os.path.basename(self.exmlPath))[0]
    ## ---------------------------------------------------------------------- 打开文件
    def OnFileTap(self, e):
        path = wui.openFileDialog()
        self.exmlPath = path
        self.initPropList()
    
    ## ---------------------------------------------------------------------- 点击左侧属性列表
    def OnPropListItemTap(self, e):
        self.updatePropShowInfo()
        self.updateEventList()
    
    ## ---------------------------------------------------------------------- 点击中间事件列表
    def OnEventItemTap(self, e):
        if len(self.list.selectIndex) <= 0:
            print("当前未选中属性")
            return
        index = self.list.selectIndex[0]
        propName = self.list.dataProvider[index]
        propInfo = self.propMap.get(propName)
        propInfo.updateEventArray(self.eventList.selectIndex)
        self.refreshTemplateContent()
    
    ## ---------------------------------------------------------------------- 点击生成按钮
    def OnOkBtn(self, e):
        if self.area.text2.strip() == "":
            wui.alert("保存失败", "先选择文件和模板")
            return
        path = self.saveDir + self.exmlName + ".ts"
        with open(path + "", "w", encoding="utf-8") as f:
            f.write(self.area.text2)
            time.sleep(1) # 停顿一秒，假装很努力在生成~
            wui.alert("保存成功", "保存地址为 " + self.saveDir)
    
    ## ---------------------------------------------------------------------- 拖拽文件回调
    def OnDragFile(self, path):
        self.resetDataAndView()
        path = path[0].decode("gbk")
        self.exmlPath = path
        self.initPropList()

if __name__ == "__main__":
    d = Demo()
