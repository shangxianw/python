import os

class FolderData:
    def __init__(self):
        self.dir = ""
        self.folderName = ""
    
    def packData(self, dir:str):
        self.dir = dir
        self.folderName = os.path.basename(self.dir)
    
    def destroy(self):
        pass