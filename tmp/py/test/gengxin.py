import os;
import shutil;
import time;
from FileUtils import FileUtils;
# import pysvn;

toDir   = "D:/work/EgerPro_5_2_9/protobuf/protofile/";
fromDir = "D:/work/code/common/msg/";
fromFile = ["messageId.proto","common.proto","client2logic.proto"];
toFile   = ["messageId.proto","common.proto","client2logic.proto"];


print("\n");
print(" ================================================= 首先更新一下协议");
os.system("start "" D:\work\code\common\msg");
os.system("pause");

print("\n\n");
print(" ================================================= 然后更新一下复制文件");
for i in range(len(fromFile)):
    fromFile[i] = fromDir + fromFile[i];
    toFile[i]   = toDir   + toFile[i];

for i in range(len(fromFile)):
    print("正在复制 " + fromFile[i]);
    print("      到 " + toFile[i]);
    shutil.copy(fromFile[i],toFile[i]);
    time.sleep(1);
print("复制完成");

time.sleep(2);
print("\n");
print(" ================================================= 接着修改文件头");
def modifyFile(tarFile):
    f = FileUtils.Open(tarFile,"r");
    content = FileUtils.Read(f);
    FileUtils.Close(f);
    newContent = content.replace("msgdef","Protocol",1);
    f = FileUtils.Open(tarFile,"w");
    FileUtils.Write(f,newContent);
    FileUtils.Close(f);
    time.sleep(1);
for i in range(len(toFile)):
    modifyFile(toFile[i]);
    print("修改 " + toFile[i] + "完成");

time.sleep(2);
print("\n");
print(" ================================================= 最后编译");
os.system("echo 正在编译...");
os.system("cd /d D:\work\EgerPro_5_2_9 & pb-egret generate");
os.system("echo 编译完成!");
os.system("pause");