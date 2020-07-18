class IDManager(object):
	id = 0
	def __init__(self):
		super(IDManager, self).__init__()
		
	def init(self):
		self.id = 0

	def getNewId(self):
		self.id += 1
		return self.id

	Instance = None
	@classmethod
	def Ins(cls):
		if IDManager.Instance is None:
			IDManager.Instance = IDManager()
		return IDManager.Instance


# print(IDManager.Ins().getNewId())
# print(IDManager.Ins().getNewId())
# print(IDManager.Ins().getNewId())