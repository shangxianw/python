import win32con
import win32gui
import os
import wui
import src.FolderData as FolderData
import pyperclip as paste
import system_hotkey as hotkey

class Main:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.baseDir = "./data/"
        self.fileType = ".txt"
        self.folderArray = []
        self.fileArray = []
        self.winName = "wsx的剪切板"

        self.win = wui.Panel()
        self.win.setTitle(self.winName)
        self.win.setSize(1070, 610)
        self.win.setResizeAble(False, False)
        self.win.setMinBtnCB(self.showWinMin)
        # self.win.protocol("WM_DELETE_WINDOW", self.showWinMin) # 点击右上角关闭按钮
        # self.win.protocol("WM_MIN_WINDOW", self.showWinMin) # 点击右上角关闭按钮
        # self.win.bind("<FocusOut>", self.OnWinFocusOut)
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
        hk = hotkey.SystemHotkey()
        hk.register(('control', '1'), callback = self.OnHotKeyCB)

        self.setBox3EditStyle(False)
        self.showBox1Content()

        self.box1.addEventListener(wui.Event.ITEM_SELECT, self.OnBox1ItemTap)
        self.box1.addEventListener(wui.TouchEvent.RIGHT_TAP, self.OnBox1RightTap)
        self.box2.addEventListener(wui.Event.ITEM_SELECT, self.OnBox2ItemTap)
        self.box2.addEventListener(wui.TouchEvent.RIGHT_TAP, self.OnBox2RightTap)
        self.box2.addEventListener(wui.TouchEvent.DOUBLE_TAP, self.OnBox2DoubleTap)
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
        if dir == "":
            self.box2.dataProvider = self.fileArray
            return
        fileArray = os.listdir(dir)
        for file in fileArray:
            path = dir + file
            if os.path.isfile(path) is True:
                fileName = file.split(".")[0]
                self.fileArray.append(fileName)
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
    
    def resetContent(self):
        self.showBox1Content()
        self.showBox2Content("")
        self.setBox3Content("")
        self.setBox3EditStyle(False)
    
    def setBox3Content(self, content:bool):
        self.box3.editable = True
        self.box3.text2 = content
        self.box3.editable = False
    
    def getFilePath(self):
        folderName = self.folderArray[self.box1.selectIndex[0]]
        fileName = self.fileArray[self.box2.selectIndex[0]]
        path = self.baseDir + folderName + "/" + fileName + self.fileType
        return path
    
    def OnCreateGroup(self):
        folderName = wui.askAlert("新建分组", "输入分组名")
        dir = self.baseDir + folderName
        os.mkdir(dir)
        self.box1.addItem(folderName)
    
    def OnDeleteGroup(self):
        if len(self.box1.selectIndex) <= 0:
            wui.alert("错误", "请选择某项进行删除")
            return
        folderName = self.folderArray[self.box1.selectIndex[0]]
        dir = self.baseDir + folderName
        fileArray = os.listdir(dir)
        for file in fileArray:
            path = dir + "/" + file
            os.remove(path)
        os.rmdir(dir)
        self.resetContent()
    
    def OnCreateFile(self):
        if len(self.box1.selectIndex) <= 0:
            wui.alert("错误", "请选择某个分组")
            return
        file = wui.askAlert("新建剪切", "输入剪切名")
        folderName = self.folderArray[self.box1.selectIndex[0]]
        path = self.baseDir + folderName + "/" + file + self.fileType
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
        self.box2.addItem(file)
    
    def OnDeleteFile(self):
        if len(self.box2.selectIndex) <= 0:
            wui.alert("错误", "请选择某项进行删除")
            return
        fileName = self.fileArray[self.box2.selectIndex[0]]
        path = self.getFilePath()
        os.remove(path)
        self.box2.removeItem(fileName)
        self.setBox3Content("")
    
    ## ---------------------------------------------------------------------- 最小化
    def showWinMin(self):
        wndtitle = self.winName
        wndclass = None
        wnd = win32gui.FindWindow(wndclass, wndtitle)
        win32gui.ShowWindow(wnd, win32con.SW_HIDE)
    
    ## ---------------------------------------------------------------------- 激活
    def showWinActive(self):
        wndtitle = self.winName
        wndclass = None
        wnd = win32gui.FindWindow(wndclass, wndtitle)
        win32gui.ShowWindow(wnd, win32con.SW_SHOWDEFAULT)

    ## ---------------------------------------------------------------------- Event
    ## ---------------------------------------------------------------------- 点击左侧
    def OnBox1ItemTap(self, e):
        if len(self.box1.selectIndex) <= 0:
            return
        folderName = self.folderArray[self.box1.selectIndex[0]]
        dir = self.baseDir + folderName + "/"
        self.showBox2Content(dir)
        self.setBox3Content("")
        self.setBox3EditStyle(False)
    
    ## ---------------------------------------------------------------------- 右键左侧
    def OnBox1RightTap(self, e):
        menubar = wui.Menu(self.win, tearoff=False)
        menubar.addCommand('新建分组', self.OnCreateGroup)
        menubar.addCommand('删除分组', self.OnDeleteGroup)
        menubar.setPos(e.x_root, e.y_root)
    
    ## ---------------------------------------------------------------------- 点击中间
    def OnBox2ItemTap(self, e):
        if len(self.box2.selectIndex) <= 0:
            return
        path = self.getFilePath()
        self.showBox3Content(path)
        self.setBox3EditStyle(False)
    
    ## ---------------------------------------------------------------------- 右键中间
    def OnBox2RightTap(self, e):
        menubar = wui.Menu(self.win, tearoff=False)
        menubar.addCommand('新建剪切', self.OnCreateFile)
        menubar.addCommand('删除剪切', self.OnDeleteFile)
        menubar.setPos(e.x_root, e.y_root)
    
    ## ---------------------------------------------------------------------- 双击中间
    def OnBox2DoubleTap(self, e):
        paste.copy(self.box3.text2)
        self.showWinMin()

    ## ---------------------------------------------------------------------- 双击右侧
    def OnBox3DoubleTap(self, e):
        if len(self.box1.selectIndex) <= 0 or len(self.box2.selectIndex) <= 0:
            wui.alert("错误", "没有选中的剪切项")
            return
        flag = bool(1 - self.box3.editable)
        self.box3.editable = flag
        self.setBox3EditStyle(flag)

        if flag is False: # 双击保存
            path = self.getFilePath()
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.box3.text2)
    
    ## ---------------------------------------------------------------------- 窗口失去焦点
    def OnWinFocusOut(self, e):
        self.showWinMin()
    
    ## ---------------------------------------------------------------------- 键盘监听
    def OnHotKeyCB(self, e):
        self.showWinActive()
    
    def destroy(self):
        self.box1.removeEventListener(wui.Event.ITEM_SELECT)
        self.box2.removeEventListener(wui.Event.ITEM_SELECT)
        self.box3.removeEventListener(wui.TouchEvent.DOUBLE_TAP)

if __name__ == "__main__":
    d = Main()