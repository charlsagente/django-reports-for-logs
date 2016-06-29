__author__ = 'charls'
from logmanagement.parser.InputsHandler import InputsHandler
from logmanagement.parser.logs_parsers.TomcatParser.Logs import Logs
from logmanagement.parser.logs_parsers.LogsParserBase import LogsParserBase
from logmanagement.parser.LogsDictionary import *

from logmanagement.parser.logs_parsers.TomcatParser.ConstantsRE import REGEX_TOMCAT_TIMESTAMP
import os
import re
import copy


class LogsParserTomcat(LogsParserBase):

    def __init__(self):
        self.__inputData = InputsHandler()
        self.in_memory_logs = Logs()

    def iterate_file_and_return_log_types(self,file,*args,**kwargs):
        LogsParserBase.iterate_file_and_return_log_types(self,file,*args,**kwargs)


    def folders_iteration(self,start_date,end_date):
        folder_path = os.path.join(self.__inputData.path_for_filesystem,
                                             MAIN_FOLDERS['tomcat_folder'])
        for file in os.listdir(folder_path):
            try:
                self.iterate_file_and_return_log_types(os.path.join(folder_path, file), file,
                                                       returning_function=self.parse_and_count_errors)
            except Exception as ex:
                print ex

        return copy.deepcopy(self.in_memory_logs.LogData)

    def parse_and_count_errors(self,line,log_level,*args):
        r = re.match(REGEX_TOMCAT_TIMESTAMP, line)
        if r:
            self.in_memory_logs.add_error_log(log_level,r.group("date"),*args)
        else:
            self.in_memory_logs.add_counted_errors_for_tomcat(log_level,*args)