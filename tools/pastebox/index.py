import os
import wui2 as wui
import src.FolderData as FolderData

class Main:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.baseDir = "./data/"
        self.folderArray = []
        self.fileArray = []

        self.win = wui.Panel()
        self.win.setTitle("wsx的粘贴板")
        self.win.setSize(1070, 610)
        self.win.resizable(False, False)
        self.initView()
        self.win.mainloop()
    
    def initView(self):
        self.box1 = wui.SimpleList(self.win)
        self.box1.x = 5
        self.box1.y = 5
        self.box1.width = 150
        self.box1.height = 600

        self.box2 = wui.SimpleList(self.win)
        self.box2.x = 160
        self.box2.y = 5
        self.box2.width = 300
        self.box2.height = 600

        self.box3 = wui.InputArea(self.win)
        self.box3.x = 465
        self.box3.y = 5
        self.box3.width = 600
        self.box3.height = 600
        self.box3.selectFg = wui.Color.Black

        self.initData()
    
    def initData(self):
        self.setBox3EditStyle(False)
        self.showBox1Content()

        self.box1.addEventListener(wui.Event.ITEM_SELECT, self.OnBox1ItemTap)
        self.box2.addEventListener(wui.Event.ITEM_SELECT, self.OnBox2ItemTap)
        self.box3.addEventListener(wui.TouchEvent.DOUBLE_TAP, self.OnBox3DoubleTap)
    
    def showBox1Content(self):
        self.folderArray = []
        fileArray = os.listdir(self.baseDir)
        for file in fileArray:
            path = self.baseDir + file
            if os.path.isdir(path) is True:
                self.folderArray.append(file)
        self.box1.dataProvider = self.folderArray
    
    def showBox2Content(self, dir:str):
        self.fileArray = []
        fileArray = os.listdir(dir)
        for file in fileArray:
            path = dir + file
            if os.path.isfile(path) is True:
                self.fileArray.append(file)
        self.box2.dataProvider = self.fileArray
    
    def showBox3Content(self, path:str):
        self.box3.text2 = ""
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            self.setBox3Content(content)

    def setBox3EditStyle(self, canEdit:bool):
        if canEdit is False:
            self.box3.editable = False
            self.box3.bg = wui.Color.LightGrey
            self.box3.selectBg = wui.Color.LightGrey
        else:
            self.box3.editable = True
            self.box3.bg = wui.Color.White
            self.box3.selectBg = wui.Color.LightBlue
    
    def setBox3Content(self, content:bool):
        self.box3.editable = True
        self.box3.text2 = content
        self.box3.editable = False

    ## ---------------------------------------------------------------------- Event
    ## ---------------------------------------------------------------------- 点击左侧
    def OnBox1ItemTap(self, e):
        if len(self.box1.selectIndex) <= 0:
            return
        folderName = self.folderArray[self.box1.selectIndex[0]]
        dir = self.baseDir + folderName + "/"
        self.showBox2Content(dir)
        self.setBox3Content("")
    
    ## ---------------------------------------------------------------------- 点击中间
    def OnBox2ItemTap(self, e):
        if len(self.box2.selectIndex) <= 0:
            return
        folderName = self.folderArray[self.box1.selectIndex[0]]
        fileName = self.fileArray[self.box2.selectIndex[0]]
        path = self.baseDir + folderName + "/" + fileName
        self.showBox3Content(path)
    
    ## ---------------------------------------------------------------------- 双击右侧
    def OnBox3DoubleTap(self, e):
        if len(self.box1.selectIndex) <= 0 or len(self.box2.selectIndex) <= 0:
            return
        flag = bool(1 - self.box3.editable)
        self.box3.editable = flag
        self.setBox3EditStyle(flag)
    
    def destroy(self):
        self.box1.removeEventListener(wui.Event.ITEM_SELECT)
        self.box2.removeEventListener(wui.Event.ITEM_SELECT)
        self.box3.removeEventListener(wui.TouchEvent.DOUBLE_TAP)

if __name__ == "__main__":
    d = Main()