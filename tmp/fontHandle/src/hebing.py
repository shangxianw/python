import os
import time
import sys
# sys.argv = ["hebing.py", "../font/", "D:/work/code/client/EgerPro_5_2_9/"];
#字体目录
fontDir = sys.argv[1];
#项目需要提取的文件夹地址
oriDir = [
	sys.argv[2] + "./src/",
	sys.argv[2] + "./resource/ui/",
	sys.argv[2] + "./resource/config/"
]
# oriDir = [
	# "D:\\work\\code\\client\\EgerPro_5_2_9\\src\\",
	# "D:\\work\\code\\client\\EgerPro_5_2_9\\resource\\ui\\",
	# "D:\\work\\code\\client\\EgerPro_5_2_9\\resource\\config\\"
# ]

print(fontDir)
print(oriDir)

# main_ttf 需要剔除提取的文件
banFiles = [
	"banwords.json",
	"namedata.json"
];
# desc_ttf 需要剔除提取的文件
banFiles2 = [
	"banwords.json",
];
# 匹配文件
formatArray = [".exml", ".ts", ".json"];
# 临时生成的文件，程序结束后会自动删掉
tarPath = "./hebing_main.html";
tarPath2 = "./hebing_desc.html";

##########################################################################
## 文件格式
txt  = '<html>\n<head>\n'
txt += '<style>\n'
txt	+= '	@font-face{\n'
txt += '		font-family: "main_font";\n'
txt += '		src: url("' + fontDir + 'main_font.ttf");\n'
txt += '		font-display: swap;\n'
txt += '	}\n'
txt += '</style>\n'
txt += '</head>\n<body>\n'
txt += '    <div style="font-family:' + "'main_font'" + '">\n';

cnT  = '';

enT  = '\n	</div></div>\n'
enT += '</body></html>';
## 文件格式2
txt2  = '<html>\n<head>\n'
txt2 += '<style>\n'
txt2	+= '	@font-face{\n'
txt2 += '		font-family: "desc_font";\n'
txt2 += '		src: url("' + fontDir + 'desc_font.ttf");\n'
txt2 += '		font-display: swap;\n'
txt2 += '	}\n'
txt2 += '</style>\n'
txt2 += '</head>\n<body>\n'
txt2 += '    <div style="font-family:' + "'desc_font'" + '">\n';

cnT2  = '';

enT2  = '\n	</div></div>\n'
enT2 += '</body></html>';
##########################################################################

class MainHB:
	def openFd(self, dir):
		fileArray = os.listdir(dir);
		for ff in fileArray:
			newDir = dir + ff;

			if os.path.isdir(newDir) is True:
				self.openFd(newDir + "/");
			else:
				try:
					formats = os.path.splitext(newDir)[1]
					a, file = os.path.split(newDir);
					print(file)
					if  (formats in formatArray) is True and (file in banFiles) is False:
						with open(newDir, "r", encoding="utf-8") as f:
							self.addTxt(f.read());
				except IndexError:
					pass;

	def addTxt(self, t):
		global cnT;
		cnT += t;

	def start(self):
		for dirr in oriDir:
			self.openFd(dirr);
		global cnT;
		cnT = cnT.replace("<", "a");
		cnT = cnT.replace(">", "b");
		cnT = cnT.replace("/", "c");
		cnT = cnT.replace("(", "d");
		cnT = cnT.replace(")", "e");
		cnT = cnT.replace(" ", "");
		cnT = cnT.replace("\n", "");
		cnT = cnT.replace("		", "");
		cnT = cnT.replace("	", "");

		tarTxt = txt + cnT + enT;
		f = open(tarPath, "w", encoding="utf-8");
		f.write(tarTxt);
		f.close();
		
		# dir_path = os.path.dirname(os.path.abspath(__file__));
		os.system("font-spider " + tarPath);

class DescHB:
	def openFd(self, dir):
		fileArray = os.listdir(dir);
		for ff in fileArray:
			newDir = dir + ff;

			if os.path.isdir(newDir) is True:
				self.openFd(newDir + "/");
			else:
				try:
					formats = os.path.splitext(newDir)[1];
					b, file2 = os.path.split(newDir);
					print(file2)
					if  (formats in formatArray) is True and (file2 in banFiles2) is False:
						with open(newDir, "r", encoding="utf-8") as f:
							self.addTxt(f.read());
				except IndexError:
					pass;

	def addTxt(self, t):
		global cnT2;
		cnT2 += t;

	def start(self):
		for dirr in oriDir:
			self.openFd(dirr);
		global cnT2;
		cnT2 = cnT2.replace("<", "a");
		cnT2 = cnT2.replace(">", "b");
		cnT2 = cnT2.replace("/", "c");
		cnT2 = cnT2.replace("(", "d");
		cnT2 = cnT2.replace(")", "e");
		cnT2 = cnT2.replace(" ", "");
		cnT2 = cnT2.replace("\n", "");
		cnT2 = cnT2.replace("		", "");
		cnT2 = cnT2.replace("	", "");

		tarTxt = txt2 + cnT2 + enT2;
		f = open(tarPath2, "w", encoding="utf-8");
		f.write(tarTxt);
		f.close();
		
		# dir_path = os.path.dirname(os.path.abspath(__file__));
		os.system("font-spider " + tarPath2);
		os.remove(tarPath);
		os.remove(tarPath2);

# if "__name__" == __main__:
m =MainHB();
m.start();

d =DescHB();
d.start();