import os

oriDir = [
	"D:/work/code/client/EgerPro_5_2_9/src/",
	"D:/work/code/client/EgerPro_5_2_9/resource/ui/",
	"D:/work/code/client/EgerPro_5_2_9/resource/config/"
]
formatArray = [".exml", ".ts"];
tarPath = "D:/wsx/python/hebing.html";

##########################################################################
## 文件格式
txt  = '<html>\n<head>\n'
txt += '<style>\n'
txt	+= '	@font-face{\n'
txt += '		font-family: "main_font";\n'
txt += '		src: url("./font/main_font.ttf");\n'
txt += '		font-display: swap;\n'
txt += '	}\n'
txt += '	@font-face{\n'
txt += '		font-family: "desc_font";\n'
txt += '		src: url("./font/desc_font.ttf");\n'
txt += '		font-display: swap;\n'
txt += '	}\n'
txt += '</style>\n'
txt += '</head>\n<body>\n'
txt += '    <div style="font-family:' + "'main_font'" + '"><div style="font-family:' + "'desc_font'" + '">\n';

cnT  = '';

enT  = '\n	</div></div>\n'
enT += '</body></html>';
##########################################################################

def openFd(dir):
	fileArray = os.listdir(dir);
	for ff in fileArray:
		newDir = dir + ff;
		# print("======================== " + newDir);
		if os.path.isdir(newDir) is True:
			# print("======================== " + newDir + " is true");
			openFd(newDir + "/");
		else:
			# print(os.path.splitext(newDir)[1]);
			try:
				formats = os.path.splitext(newDir)[1]
				if  formats == ".exml" or formats == ".ts" or formats == ".json":
					print("====================== " + newDir);
					f = open(newDir, "r", encoding="utf-8");
					addTxt(f.read());
					f.close();
			except IndexError:
				pass;

def addTxt(t):
	global cnT;
	cnT += t;

def start():
	for dirr in oriDir:
		openFd(dirr);
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
	print(tarTxt);

	f = open(tarPath, "w", encoding="utf-8");
	f.write(tarTxt);
	f.close();

	# dir_path = os.path.dirname(os.path.abspath(__file__));
	os.system("font-spider " + tarPath);

# if "__name__" == __main__:
start();