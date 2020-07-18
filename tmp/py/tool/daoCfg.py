import os
import shutil

# 用于更新配置表
class CopyCfg(object):
	
	toolPath    = None; # 工具所在文件夹
	toolName    = None; # 工具名字
	tarPath     = None; # 源文件夹
	oriPath     = None; # 目标文件夹
	rmFileArray = None; # 不需要复制的文件列表

	def __init__(self):
		super(CopyCfg, self).__init__();
		self.init();

	######################################################################
	## 修改以下内容即可
	def init(self):
		self.toolPath    = "D:/work/design/导表/";
		self.toolName    = "导表工具.bat";
		self.oriPath     = "D:/work/design/导表/export/resource/config/";
		self.tarPath     = "D:/work/code/client/EgerPro_5_2_9/resource/config/";
		self.rmFileArray = ["serverdata.json"];
	######################################################################
	def destroy(self):
		pass;

	## ---------------------------------------------------------------------- Api
	def startCopy(self):
		oriFilePath = "";
		tarFilePath = "";
		for item in os.listdir(self.oriPath):
			oriFilePath = self.oriPath + item;
			tarFilePath = self.tarPath + item;
			
			if os.path.isfile(oriFilePath) == True and self.hasRemoveFile(item) == False:
				shutil.copyfile(oriFilePath,tarFilePath);
				print("正在复制 " + item);
		print("----------------------------------------------------------------------");
		for item in self.rmFileArray:
			print("没有参与复制的文件 " + item);
		print("----------------------------------------------------------------------");
		input("复制完成，按 回车键 关闭窗口");

	def openOriAndTarFolder(self):
		os.system('start "" ' + self.oriPath);
		os.system('start "" ' + self.tarPath);
		input("更新两个文件夹，完成后按 回车键 继续");

	def runDaoBiaoTool(self):
		os.chdir(self.toolPath);
		os.system('start "" ' + self.toolName);
		input("导表，完成后按 回车键 继续");

	## ---------------------------------------------------------------------- Tools
	def hasRemoveFile(self,fileName:str):
		for file in self.rmFileArray:
			if file == fileName:
				return True;
		return False;

if __name__ == "__main__":
	demo = CopyCfg();
	demo.openOriAndTarFolder();
	demo.runDaoBiaoTool();
	demo.startCopy();