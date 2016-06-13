__author__ = 'charls'
from sys import platform as _platform
import os
import logging
from django.conf import settings


class InputsHandler:

    def __init__(self, subfolder="seen"):
        self.__path = os.path.join(os.path.dirname(__file__),subfolder)
        self.__linux_path = os.path.join(os.environ['HOME'],"s3/logs")
        self.__windows_path = "C:\\reportsforlogs\\logs"
        self.__file = None
        self.__fingerprints = set()
        self.set_path_for_filesystem()
        if self.__path:
            self.__file = open(os.path.join(self.__path,"parsedfolders.seen"), "a+")
            self.__fingerprints.update(x.rstrip() for x in self.__file)

    def __del__(self):
        self.close()

    def get_file_contents(self, folder,file):
        self.set_path_for_filesystem()
        with open(os.path.join(self.path_for_filesystem,folder,file), 'r') as content_file:
            content = content_file.read()
        return content

    def is_already_parsed(self, file):
        if file in self.__fingerprints:
            return True
        return False


    def already_parsed(self, file):
        if file in self.__fingerprints:
            return False
        self.__fingerprints.add(file)
        if self.__file:
            self.__file.write(file + os.linesep)
        return True

    def set_path_for_filesystem(self):
        if _platform == "linux" or _platform == "linux2":
            self.path_for_filesystem = self.__linux_path

        elif _platform == "win32":
            self.path_for_filesystem = self.__windows_path

    def close(self):
        if self.__file:
            self.__file.close()

    def log(self,msg=None):
        if settings.DEBUG and msg:
            self.__logger = logging.getLogger(__name__)
            self.__logger.debug(msg)