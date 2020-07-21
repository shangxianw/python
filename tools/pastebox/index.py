import wui

class Main:
    def __init__(self):
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
        self.box1.addEventListener(wui.Event.ITEM_SELECT, self.OnBox1ItemTap)

        self.box2 = wui.SimpleList(self.win)
        self.box2.x = 160
        self.box2.y = 5
        self.box2.width = 300
        self.box2.height = 600
        self.box2.addEventListener(wui.Event.ITEM_SELECT, self.OnBox2ItemTap)

        self.box3 = wui.InputArea(self.win)
        self.box3.x = 465
        self.box3.y = 5
        self.box3.width = 600
        self.box3.height = 600
        self.box3.addEventListener(wui.TouchEvent.DOUBLE_TAP, self.OnBox3DoubleTap)
    
    def OnBox1ItemTap(self):
        pass
    
    def OnBox2ItemTap(self):
        pass
    
    def OnBox3DoubleTap(self):
        pass



if __name__ == "__main__":
    d = Main()