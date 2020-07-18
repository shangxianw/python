import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.simpledialog as dialog
import os
import pyperclip as paste
import win32gui
import win32con
import time
import system_hotkey as hotkey

class PasteBoard:
    def __init__(self):
        workDir = os.getcwd()
        os.chdir(workDir)
        self.winName = "wsx的剪切板"
        self.tmpDir = "./tmp/"
        self.currFolder = ""
        self.currFile = ""
        self.currContent = ""

        self.win = tk.Tk()
        self.win.title(self.winName)
        self.win.geometry("1080x610+100+100")
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self.callbackClose) # 点击右上角关闭按钮
        self.setHotKey()
        self.initView()
        self.showFolderList(self.tmpDir)
        self.win.mainloop()
    
    def setHotKey(self):
        hk = hotkey.SystemHotkey()
        hk.register(('control', '1'), callback = self.OnHotKeyCB)
        hk.register(('control', "2"), callback = self.OnHotKeyEsc)

    def initView(self):
        self.listBox1 = tk.Listbox(self.win) # selectmode=tk.MULTIPLE 实现多选
        self.listBox1.place(x=0, y=0, width=150, height=600)
        self.listBox1.bind("<<ListboxSelect>>", self.OnListBox1Tap)
        self.listBox1.bind("<Button-3>", self.OnListBox1Button3Tap)

        self.listBox2 = tk.Listbox(self.win)
        self.listBox2.place(x=160, y=0, width=300, height=600)
        self.listBox2.bind("<<ListboxSelect>>", self.OnListBox2Tap)
        self.listBox2.bind("<Double-Button-1>", self.OnListBox2DoubleTap)
        self.listBox2.bind("<Button-3>", self.OnListBox2Button3Tap)

        self.text = tk.Text(self.win)
        self.text.bind("<KeyRelease>", self.OnTextFocusOut)
        self.text.place(x=470, y=0, width=600, height=600)

        # self.win.bind("<FocusOut>", self.OnWinFocusOut)
    
    ## ---------------------------------------------------------------------- 显示文件夹列表
    def showFolderList(self, dir):
        fileArray = os.listdir(dir)
        for file in fileArray:
            path = dir + file
            if os.path.isdir(path) is True:
                self.listBox1.insert(tk.END, file)
    
    ## ---------------------------------------------------------------------- 显示文件列表
    def showFileList(self, dir):
        self.listBox2.delete(0, tk.END)
        self.text.delete("1.0", tk.END)
        fileArray = os.listdir(dir)
        for file in fileArray:
            fileName = file.split(".")[0]
            path = dir + file
            if os.path.isfile(path) is True:
                self.listBox2.insert(tk.END, fileName)
    
    ## ---------------------------------------------------------------------- 显示内容
    def showFileContent(self, path):
        self.text.delete("1.0", tk.END)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            self.text.insert(tk.END, content)
            self.currContent = content
            paste.copy(self.currContent)
    
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
    
    ## ---------------------------------------------------------------------- 创建分组
    def OnCreateNew(self):
        flag = dialog.askstring('新建分组', '输入组名:') # initialvalue='字符串'
        if flag is None or flag is False:
            return
        if self.checkGroupValide(flag) is False:
            return
        dir = self.tmpDir + flag
        os.mkdir(dir)
        self.listBox1.insert(tk.END, flag)
    
    def OnDeleteGroup(self):
        indexArray = self.listBox1.curselection()
        index = indexArray[0]
        self.listBox1.delete(index)
        self.listBox2.delete(0, tk.END)

        dir = self.tmpDir + self.currFolder
        fileArray = os.listdir(dir)
        for file in fileArray:
            path = dir + "/" + file
            os.remove(path)
        os.rmdir(dir)
        self.currFolder = ""
    
    ## ---------------------------------------------------------------------- 创建剪切
    def OnCreateNewFile(self):
        flag = dialog.askstring('新建剪切', '输入剪切名:')
        if flag is None or flag is False:
            return
        if self.checkFileValide(flag) is False:
            return
        path = self.tmpDir + self.currFolder + "/" + flag + ".txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
        self.listBox2.insert(tk.END, flag)
    
    def OnDeleteFile(self):
        indexArray = self.listBox2.curselection()
        index = indexArray[0]
        self.listBox2.delete(index)

        path = self.tmpDir + self.currFolder + "/" + self.currFile + ".txt"
        os.remove(path)
        self.currFile = ""
    
    ## ---------------------------------------------------------------------- 文本区域失去焦点
    def OnTextFocusOut(self, e):
        path = self.tmpDir + self.currFolder + "/" + self.currFile + ".txt"
        if os.path.exists(path) is False:
            print("不存在该文件")
            return
        with open(path, "w", encoding="utf-8") as f:
            content:str = self.text.get("0.0", tk.END).strip()
            f.write(content)
            # print(content)
    
    def OnWinFocusOut(self, e):
        self.showWinMin()

    ## ---------------------------------------------------------------------- 检查分组可用性
    def checkGroupValide(self, groupName:str):
        if groupName.strip() == "":
            return False
        folderArray = os.listdir(self.tmpDir)
        try:
            folderArray.index(groupName)
            return False
        except(BaseException):
            return True
    
    ## ---------------------------------------------------------------------- 检查文件可用性
    def checkFileValide(self, fileName:str):
        if fileName.strip() == "":
            return False
        folderArray = os.listdir(self.tmpDir + self.currFolder + "/")
        try:
            folderArray.index(fileName)
            return False
        except(BaseException):
            return True

    ## 键盘监听
    def OnHotKeyCB(self, e):
        # print("==================================" + str(time.gmtime()))
        self.showWinActive()
    
    def OnHotKeyEsc(self, e):
        # print("==================================1")
        self.showWinMin()
    

    ## ---------------------------------------------------------------------- event
    ## ---------------------------------------------------------------------- 点击文件夹列表
    def OnListBox1Tap(self, e):
        indexArray = self.listBox1.curselection()
        index = indexArray[0]
        self.currFolder = self.listBox1.get(index)
        dir = self.tmpDir + self.currFolder + "/"
        self.showFileList(dir)
    
    ## ---------------------------------------------------------------------- 右键文件夹列表
    def OnListBox1Button3Tap(self, e):
        menubar = tk.Menu(self.win, tearoff=False)
        menubar.add_command(label='新建分组', command=self.OnCreateNew)
        menubar.add_command(label='删除分组', command=self.OnDeleteGroup)
        menubar.post(e.x_root, e.y_root)
    
    ## ---------------------------------------------------------------------- 右键文件列表
    def OnListBox2Button3Tap(self, e):
        menubar = tk.Menu(self.win, tearoff=False)
        menubar.add_command(label='新建剪切项', command=self.OnCreateNewFile)
        menubar.add_command(label='删除剪切项', command=self.OnDeleteFile)
        menubar.post(e.x_root, e.y_root)

    ## ---------------------------------------------------------------------- 点击文件列表
    def OnListBox2Tap(self, e):
        indexArray = self.listBox2.curselection()
        index = indexArray[0]
        self.currFile = self.listBox2.get(index)
        path = self.tmpDir + self.currFolder + "/" + self.currFile + ".txt"
        self.showFileContent(path)
    
    def OnListBox2DoubleTap(self, e):
        indexArray = self.listBox2.curselection()
        index = indexArray[0]
        self.currFile = self.listBox2.get(index)
        path = self.tmpDir + self.currFolder + "/" + self.currFile + ".txt"
        self.showFileContent(path)
        self.showWinMin()
    
    def callbackClose(self):
        self.showWinMin()

p = PasteBoard()
print("start~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
if __name__ == "__main__":
    pass