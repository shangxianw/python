# 需要确保file库存在
# 主要是处理文件内部的东西
# os库则是处理文件和目录，属于file外部的东西

# "w" 只用于写，会清空原来文件。如果文件不存在，则会创建一个。
# "r" 只用于读，没有就帮你创建一个
# "a" 追加，可写不可读，默认将指针放到最后。

# 因为w和r都是读全部或者写全部，所以光标是0.而a是追加，所以指针在最后，可以知道字符长度

class FileUtils:
	@staticmethod	def Open(fileName,mode="r"):

		return open(fileName,mode,encoding='utf-8');
	
	def Write(f,content):
		return f.write(content);

	# 读取文件内容，len为长度，不管英文还是中文，都是读取长度
	def Read(f,len=None):
		return f.read(len);
	
	# 读取所有hang内容，包括'\n'
	def ReadLines(f):
		return f.readlines();
	
	def Close(f):
		return f.close();
	
	def demo(f,s):
		return f.seek(s);