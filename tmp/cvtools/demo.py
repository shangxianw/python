import os
import tkinter as tk

class CV:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.templateDir = "./template/"
        self.win = tk.Tk()
        self.win.title("模板工具")
        self.win.geometry("700x800")
        self.initView()
        self.win.mainloop()
    
    def initView(self):
        fileArray = os.listdir(self.templateDir)
        index = 0
        for file in fileArray:
            path = self.templateDir + file
            fileName = file.split(".")[0]
            fileType = file.split(".")[1]

            if os.path.isfile(path) is True and fileType == "txt":
                btn = tk.Button(self.win, text=fileName, width=20) # , command=lambda:self.OnBtnClick(a=btn)
                btn["command"] = lambda:self.OnBtnClick(a=btn)
                btn.grid(column=0, row=index)
                index += 1
        self.showText = tk.Text(self.win, bd=5)
        self.showText.place(x=180, y=0)
    
    def OnBtnClick(self, a:tk.Button):
        path = self.templateDir + a["text"] + ".txt"
        with open(path, "r", encoding="utf-8") as f:
            self.showText.delete(1.0,tk.END)
            self.showText.insert(tk.END, f.read())


demo = CV()
