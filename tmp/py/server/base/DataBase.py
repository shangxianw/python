from Hash import Hash
from IDManager import IDManager
from MsgManager import MsgManager


class DataBase:
    id = 0
    def __init__(self):
        super(DataBase, self).__init__()
        self.init();

    def init(self):
        self.id = IDManager.Ins().getNewId()

    def destroy(self):
        self.id = 0

    def addAttrListener(self):
        pass

    def removeAttrListener(self, attrName: str):
        pass

    def removeAllAttrListener(self):
        pass

    def dispatch(self):
        pass

DataBase()