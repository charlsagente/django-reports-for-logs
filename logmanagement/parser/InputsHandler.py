__author__ = 'charls'
from sys import platform as _platform
import os


class InputsHandler:
    def __init__(self):
        self.__linux_path="/mnt/logs"
        self.__windows_path="C:\reportsforlogs\logs"

    def get_data_from_filesystem(self):
        if _platform == "linux" or _platform == "linux2":
            files=self.list_files(self.__linux_path)

        elif _platform == "win32":
            files=self.list_files(self.__windows_path)

    #Asuming S3 is now configured like a mounted device, check the script.sh in $HOME/clonedrepos/initscript
    def list_files(self,path):
        files = []
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                files.append(name)
                print path+os.sep+name
            else:
                self.list_files(os.path.join(path,name))

