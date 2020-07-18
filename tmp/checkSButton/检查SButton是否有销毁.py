
import os

class CheckSButtn:
    def __init__(self):
        self.projectDir = "D:/work/code/client/EgerPro_5_2_9"

    def start(self):
        dir = os.listdir(self.projectDir)
        for key in dir:
            if key == "src":
                tarDir = self.projectDir + "/" + key + "/"
                self.searchTsFile(tarDir)
    
    def searchTsFile(self, dir:str):
        fileList = os.listdir(dir)
        for fileName in fileList:
            newDir = dir + "/" + fileName
            if os.path.isdir(newDir) is True:
                self.searchTsFile(newDir)
            elif os.path.isfile(newDir) is True and os.path.splitext(newDir)[1] == ".ts":
                self.openFileAndFindTargetId(newDir)
    
    def openFileAndFindTargetId(self, tsPath:str):
        with open(tsPath, "r", encoding="utf-8") as f:
            contentArray = f.readlines()
            for content in contentArray:
                if content.find("SGroup") >= 0:
                    print(tsPath)
                    break

a = CheckSButtn()
a.start()
