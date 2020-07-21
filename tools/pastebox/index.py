import os
import wui2 as wui
import src.FolderData as FolderData

class Main:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.baseDir = "./data/"
        self.folderArray = []

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
        fileArray = os.listdir(self.baseDir)
        for file in fileArray:
            if os.path.isfile(file) is False:
                self.folderArray.append(file)
        self.box1.dataProvider = self.folderArray
    
    def showBox2Content(self, folder):
        pass

    def setBox3EditStyle(self, canEdit:bool):
        if canEdit is False:
            self.box3.editable = False
            self.box3.bg = wui.Color.LightGrey
            self.box3.selectBg = wui.Color.LightGrey
        else:
            self.box3.editable = True
            self.box3.bg = wui.Color.White
            self.box3.selectBg = wui.Color.LightBlue

    ## ---------------------------------------------------------------------- Event
    ## ---------------------------------------------------------------------- 点击左侧
    def OnBox1ItemTap(self, e):
        pass
    
    ## ---------------------------------------------------------------------- 点击中间
    def OnBox2ItemTap(self, e):
        pass
    
    ## ---------------------------------------------------------------------- 双击右侧
    def OnBox3DoubleTap(self, e):
        flag = bool(1 - self.box3.editable)
        self.box3.editable = flag
        self.setBox3EditStyle(flag)
    
    def destroy(self):
        self.box1.removeEventListener(wui.Event.ITEM_SELECT)
        self.box2.removeEventListener(wui.Event.ITEM_SELECT)
        self.box3.removeEventListener(wui.TouchEvent.DOUBLE_TAP)

        for info in self.folderArray:
            info.destroy()
            info = None
        self.folderArray = None

if __name__ == "__main__":
    d = Main()