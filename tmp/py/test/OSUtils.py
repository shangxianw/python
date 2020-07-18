import os;

class OSUtils:
	@staticmethod
	# ---------------------------------------------------------------------- 目录
	# 增删查
	# 添加一个目录
	def AddDir(path):
		return os.mkdir(path);
	
	def RemoveDir(path):
		return os.removedirs(path);

	# 是否存在该目录(即传入路径会检测是否有该目录，而不是单纯判断path的格式)
	def HasDir(path):
		if OSUtils.IsFile(path) == True:
			return;
		return os.path.exists(path);
	
	# 返回目录下(文件&文件夹列表)
	def GetDir(path):
		return os.listdir(path);

	# ---------------------------------------------------------------------- 文件
	# 增删查
	def AddFile(path,mode="w"):
		return open(path,mode);

	def RemoveFile(path):
		return os.remove(path);
	
	def HasFile(path):
		if OSUtils.IsDir() == True:
			return;
		return os.path.exists(path);
	
	# 返回文件名
	def GetFile(path):
		return os.path.basename(path);

	# ---------------------------------------------------------------------- 检验工具 
	# 切换当前目录到指定目录
	def ChangeWorkDir(path):
		return os.chdir(path);
	
	# 获取当前工作目录
	def CurrWorkDir():
		return os.getcwd();

	# 是否为目录
	def IsDir(path):
		return os.path.isdir(path);

	# 是否为文件
	def IsFile(path):
		return os.path.isfile(path);

	
	