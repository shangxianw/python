from .Label import Label
from .Group import Group
from .Button import Button

class IOCom(Group):
    def __init__(self, master):
        super(Group, self).__init__(master, bg="yellow")
        self.initView()
        self.initData()
    
    def initView(self):
        self.group = Group(self)
        self.group.x = 0
        self.group.y = 0

        self.btn1 = Button(self)
        self.btn1.x = 0
        self.btn1.y = 0
        self.btn1.label = "点我选择文件"

        self.lb1 = Label(self)
        self.lb1.x = 90
        self.lb1.y = 3
        self.lb1.text2 = "文件地址"

        self.btn2 = Button(self)
        self.btn2.x = 0
        self.btn2.y = 40
        self.btn2.label = "选择保存位置"

        self.lb2 = Label(self)
        self.lb2.x = 90
        self.lb2.y = 43
        self.lb2.text2 = "保存地址"

        self.width = 400
        self.height = 70
    
    def initData(self):
        pass