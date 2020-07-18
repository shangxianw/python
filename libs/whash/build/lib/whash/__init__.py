class WHash:
    def __init__(self):
        self.init()
    
    def init(self):
        self.keyArray = []
        self.valueArray = []
    
    def destroy(self):
        self.keyArray = []
        self.valueArray = []
    
    def set(self, key, value):
        self.keyArray.append(key)
        self.valueArray.append(value)
    
    def get(self, key):
        try:
            index = self.keyArray.index(key)
            return self.valueArray[index]
        except(BaseException):
            return None

    def has(self, key):
        try:
            self.keyArray.index(key)
            return True
        except(BaseException):
            return False
    
    def remove(self, key):
        try:
            index = self.keyArray.index(key)
            del self.keyArray[index]
            del self.valueArray[index]
        except(BaseException):
            return False
    
    def values(self):
        return self.valueArray
    
    def keys(self):
        return self.keyArray