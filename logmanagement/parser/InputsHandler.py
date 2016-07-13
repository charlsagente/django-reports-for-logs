__author__ = 'charls'
from sys import platform as _platform
import os
import logging
from django.conf import settings


class InputsHandler:

    def __init__(self):
        self.set_path_for_filesystem()

    def get_file_contents(self, folder,file):
        self.set_path_for_filesystem()
        with open(os.path.join(self.path_for_filesystem,folder,file), 'r') as content_file:
            content = content_file.read()
        return content

    def set_path_for_filesystem(self, subfolder="logs"):
        if _platform == "linux" or _platform == "linux2":
            self.path_for_filesystem = os.path.join(os.environ['HOME'], "s3", subfolder)

        elif _platform == "win32":
            self.path_for_filesystem = os.path.join("C:\\reportsforlogs", subfolder)

    def log(self,msg):
        if settings.DEBUG and msg:
            self.__logger = logging.getLogger(__name__)
            self.__logger.debug(msg)