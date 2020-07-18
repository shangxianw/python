from Hash import Hash


class MsgManager(object):
    msgMap: Hash = None  # Hash<number,[][type,callFn,thisObj,param]>

    def __init__(self):
        super(MsgManager, self).__init__()
        self.init()

    def init(self):
        self.msgMap = Hash()

    def destroy(self):
        for key, callArray in self.msgMap:
            for index, call in callArray:
                call[0] = None
                call[1] = None
                call[2] = None
                call[3] = None
            callArray = None
        self.msgMap.destroy()
        self.msgMap = None

    # ---------------------------------------------------------------------- Api
    def addMsgListenter(self, type, callFn, thisObj, param=None):
        if type is None or callFn is None or thisObj is None:
            return False
        if self.msgMap.has(type) is False:
            self.msgMap.add(type, [])

        msgArray = self.msgMap.get(type)
        for key, callArray in msgArray:
            for index, call in callArray:
                if call[0] == type and call[1] == callFn and call[2] == thisObj:
                    return False

        newCall = []
        newCall.append(type)
        newCall.append(callFn)
        newCall.append(thisObj)
        newCall.append(param)
        msgArray.append(newCall)
        return True

    def removeMsgListenter(self, type, callFn, thisObj):
        if type is None or callFn is None or thisObj is None:
            return False

        if self.msgMap.has(type) is False:
            return False

        msgArray = self.msgMap.get(type)
        for call in msgArray:
            if call[0] == type and call[1] == callFn and call[2] == thisObj:
                call[0] = None
                call[1] = None
                call[2] = None
                call[3] = None
                call = None
                self.msgMap.clear(type)
                return True
        return False

    def removeAllListener(self):
        msgList = self.msgMap.values()
        for msgArray in msgList:
            for call in msgArray:
                call[0] = None
                call[1] = None
                call[2] = None
                call[3] = None
                call = None
            del msgArray[:]
        del msgList[:]

    def dispatch(self, type, param=None):
        if type is None:
            return False

        if self.msgMap.has(type) is False:
            return False

        msgArray = self.msgMap.get(type)
        if msgArray is None:
            return False

        for call in msgArray:
            if call is None:
                continue
            if call[3] is not None and param is not None:
                call[1](call[3], param)
            elif call[3] is not None and param is None:
                call[1](call[3])
            elif call[3] is None and param is not None:
                call[1](param)
            elif call[3] is None and param is None:
                call[1]()

    Instance = None

    @classmethod
    def Ins(cls):
        if MsgManager.Instance is None:
            MsgManager.Instance = MsgManager()
        return MsgManager.Instance


# class Demo(object):

#     def __init__(self):
#         super(Demo, self).__init__()

#     def testCall(self, a):
#         print(a)

#     def run(self):
#         MsgManager.Ins().addMsgListenter(1, self.testCall, self)
#         MsgManager.Ins().addMsgListenter(2, self.testCall, self)
#         # MsgManager.Ins().removeAllListener()
#         MsgManager.Ins().dispatch(2, "你好")


# c = Demo()
# c.run()
