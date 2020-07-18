class Hash(object):
    map = {}

    def __init__(self):
        super(Hash, self).__init__()
        self.init()

    def init(self):
        self.map = {}

    def destroy(self):
        for item in self.map:
            if(item is not None):
                item = None
        self.map = None

    # ---------------------------------------------------------------------- Api
    def add(self, key, value):
        if self.map.get(key) is not None:
            return
        self.map[key] = value

    def remove(self, key):
        if self.map.get(key) is None:
            return
        a = self.map[key]
        del self.map[key]
        return a

    def clear(self, key):
        if self.map.get(key) is not None:
            return
        self.map[key] = None
        del self.map[key]

    def has(self, key):
        return self.map.get(key) is not None

    def get(self, key):
        return self.map.get(key)

    def keys(self):
        keyArray = []
        for key in self.map:
            keyArray.append(key)
        return keyArray

    def values(self):
        valueArray = []
        for key in self.map:
            valueArray.append(self.map[key])
        return valueArray


# a = Hash(1)
# a.add("name","wsx");
# a.add("age",18);
# b = a.clear("name");
# print(b);
# print(a.values())
