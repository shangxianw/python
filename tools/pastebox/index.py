import wui2 as wui

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

        self.initData()
    
    def initData(self):
        self.box3.text2 = "dlasjdlk"
        self.box3.editable = False
        self.box3.bg = wui.Color.LightGrey

        self.box1.addEventListener(wui.Event.ITEM_SELECT, self.OnBox1ItemTap)
        self.box2.addEventListener(wui.Event.ITEM_SELECT, self.OnBox2ItemTap)
        self.box3.addEventListener(wui.TouchEvent.DOUBLE_TAP, self.OnBox3DoubleTap)
    
    ## ---------------------------------------------------------------------- Event
    ## ---------------------------------------------------------------------- 点击左侧
    def OnBox1ItemTap(self, e):
        pass
    
    ## ---------------------------------------------------------------------- 点击中间
    def OnBox2ItemTap(self, e):
        pass
    
    ## ---------------------------------------------------------------------- 双击右侧
    def OnBox3DoubleTap(self, e):
        self.box3.editable = bool(1 - self.box3.editable)
        if self.box3.editable is True:
            self.box3.bg = wui.Color.White
            self.box3.selectBg = wui.Color.LightBlue
        if self.box3.editable is False:
            self.box3.bg = wui.Color.LightGrey
            self.box3.selectBg = wui.Color.LightGrey
        print(self.box3.bg)
    
    def destroy(self):
        self.box1.removeEventListener(wui.Event.ITEM_SELECT)
        self.box2.removeEventListener(wui.Event.ITEM_SELECT)
        self.box3.removeEventListener(wui.TouchEvent.DOUBLE_TAP)

if __name__ == "__main__":
    d = Main()