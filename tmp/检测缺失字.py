from fontTools.ttLib import TTFont

fontPath = input("输入字体库的地址：")
searchStr = input("输入要查的字(多个字按空格隔开):");

try:
	font = TTFont(fontPath);
except BaseException:
	print("=============================================可能是地址不对");
	
uniMap = font['cmap'].tables[0].ttFont.getBestCmap();
count = 0;
for a in searchStr:
	flag = ord(a) in uniMap.keys();
	if flag is False:
		print("【" + a + "】是缺失字");
		count += 1;
if count == 0:
	print("没有缺失字");