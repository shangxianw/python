import zipfile
import os

def toZip():
	os.chdir("./111");
	f = zipfile.ZipFile("../testZip2.zip", "w", zipfile.ZIP_DEFLATED);
	f.write("./1.txt");
	f.write("./2.txt");
	f.write("./3.txt");
	f.close();

def unZip():
	f = zipfile.ZipFile("./testZip.zip");
	f.extractall();
	f.close();

def checkIsZip():
	fileArray = os.listdir();
	for f in fileArray:
		if zipfile.is_zipfile(f) is True:
			print(f + ":1");
		else:
			print(f + ":0");

def getName():
	a = zipfile.ZipFile("./testZip.zip");
	fileArray = a.namelist();
	for f in fileArray:
		print(f);

def test():
	os.chdir("D:\\work\\code\\client\\EgerPro_5_2_9\\bin-release\\1003开发内网-王尚贤\\1001\\1003\\res\\js");
	f = zipfile.ZipFile("../testZip3.zip", "w", zipfile.ZIP_DEFLATED);
	fileArray = os.listdir();
	for ff in fileArray:
		# print(ff);
		if zipfile.is_zipfile(ff) is False:
			f.write(ff);
			print(ff);
	f.close();

def testList():
	os.chdir("D:\\work\\code\\client\\EgerPro_5_2_9\\bin-release\\1003开发内网-王尚贤\\1001\\1003\\res\\js");
	f = zipfile.ZipFile("./testZip3.7z");
	fileArray = f.namelist();
	for ff in fileArray:
		print(ff);
	f.close();

def testUnZip():
	os.chdir("D:\\work\\code\\client\\EgerPro_5_2_9\\bin-release\\1003开发内网-王尚贤\\1001\\1003\\res");
	f = zipfile.ZipFile("./js.7z");
	f.extractall();
	f.close();


if __name__ == "__main__":
	# toZip();
	# unZip();
	# checkIsZip();
	# getName();
	# test();
	# testList();
	testUnZip();