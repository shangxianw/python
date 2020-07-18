import py7zr
import zipfile
import os

# 需要被压缩的文件夹
tarDir = "D:/work/code/client/EgerPro_5_2_9/bin-release/1003开发内网-王尚贤/1001/1003/res/js/";
# 压缩文件保存地址
saveDir = "D:/work/code/client/EgerPro_5_2_9/bin-release/1003开发内网-王尚贤/1001/1003/res/";
# 压缩文件名，仅支持 zip 和 7z
saveName = "test.zip";

def toZip():
	savePath = saveDir + saveName;
	f = zipfile.ZipFile(savePath, "w", zipfile.ZIP_DEFLATED);
	os.chdir(tarDir);
	fileArray = os.listdir();
	for ff in fileArray:
		f.write(ff);
	f.close();

def to7z():
	savePath = saveDir + saveName;
	f = py7zr.SevenZipFile(savePath, "w");
	os.chdir(tarDir);
	f.writeall("./");
	f.close();
if __name__ == "__main__":
	exName = saveName.split(".")[1];
	if exName == "zip":
		toZip();
	elif exName == "7z":
		to7z();
