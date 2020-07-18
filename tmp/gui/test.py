import tkinter as tk
import windnd
import os
import tkinter.filedialog as fd
import tkinter.messagebox as mb

class Demo:
    def __init__(self):

        self.win = tk.Tk()
        self.win.title("demo")
        self.win.geometry("400x600")
        self.start()
        self.win.mainloop()
    
    def start(self):
        self.initView()

    def initView(self):
        # py
        self.text = tk.Text(self.win, bd=5)
        self.text.place(x=0, y=0, width=400, height=100)
        windnd.hook_dropfiles(self.text, func=self.OnDragFile)
        self.btn = tk.Button(self.win, text="将py文件拖入上框或者点我选择文件", command=self.OnBtnClick)
        self.btn.place(x=0, y=100, width=400, height=40)

        # ico
        self.iconText = tk.Text(self.win, bd=5)
        self.iconText.place(x=0, y=200, width=400, height=100)
        windnd.hook_dropfiles(self.iconText, func=self.OnDragIconFile)
        self.iconBtn = tk.Button(self.win, text="将图标拖入上框或者点我选择文件\n没有则使用默认图标", command=self.OnIconBtnClick)
        self.iconBtn.place(x=0, y=300, width=400, height=40)

        #save
        self.saveEntry = tk.Entry(self.win, bd=5)
        self.saveEntry.place(x=0, y=400, width=400, height=50)
        self.saveBtn = tk.Button(self.win, text="点我选择保存地址\n没有则保存本exe相同目录", command=self.OnSaveBtnClick)
        self.saveBtn.place(x=0, y=450, width=400)

        # do
        self.doBtn = tk.Button(self.win, text="生成exe", command=self.OnDoBtnClick)
        self.doBtn.place(x=0, y=500)

    ## ---------------------------------------------------------------------- 拖拽
    def OnDragFile(self, files):
        self.text.delete(1.0,tk.END)
        for file in files:
            file = file.decode("gbk")
            
            self.text.insert(tk.END, file)
    
    def OnDragIconFile(self, files):
        self.iconText.delete(1.0,tk.END)
        for file in files:
            file = file.decode("gbk")
            self.iconText.insert(tk.END, file)
    ## ---------------------------------------------------------------------- click
    def OnBtnClick(self):
        path = fd.askopenfilename()
        self.text.delete(1.0,tk.END)
        self.text.insert(tk.END, path)
    
    def OnIconBtnClick(self):
        path = fd.askopenfilename()
        self.iconText.delete(1.0,tk.END)
        self.iconText.insert(tk.END, path)
    
    def OnSaveBtnClick(self):
        path = fd.askdirectory()
        self.saveEntry.select_clear()
        self.saveEntry.insert(tk.END, path)
    
    def OnDoBtnClick(self):
        pyPath = self.text.get("0.0", tk.END).strip()
        iconPath = self.iconText.get("0.0", tk.END).strip()
        saveDir = self.saveEntry.get().strip()

        if os.path.splitext(pyPath)[1] != ".py":
            print("py文件不对")
            return
        
        if saveDir != "" and os.path.isdir(saveDir) is False:
            print("保存地址不对")
            return
        
        if iconPath != "" and os.path.splitext(iconPath)[1] != ".ico":
            print("图标文件不对")
        
        cmd = "pyinstaller --onefile " + pyPath + " --noconsole "
        if iconPath is not "":
            cmd += " -i " + iconPath
        if saveDir is not "":
            cmd += " --distpath " + saveDir + " --workpath " + saveDir
        os.system(cmd)
        mb.showinfo("生成完成", "生成完毕！")

if __name__ == "__main__":
    d = Demo()
