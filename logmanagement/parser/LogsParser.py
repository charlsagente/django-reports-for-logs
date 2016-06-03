__author__ = 'charls'
import os
import re
from InputsHandler import InputsHandler
from Logs import Logs
from LogsDictionary import dictionary, folders,logs

class LogsParser:

    def __init__(self):
        self.__inputData = InputsHandler()
        self.regex_internal_errors_mw_int = [re.compile(p) for p in dictionary['internal-errors-mw-int']]
        self.regex_errors_mw_int = [re.compile(p) for p in dictionary['errors-mw-int']]
        self.in_memory_logs = Logs()

    def parse_backup_iteration(self, subfolder = folders['middleware_backups_folder']):
        folder_path = os.path.join(self.__inputData.path_for_filesystem, subfolder)
        for log_files in os.listdir(folder_path):
            if not self.__inputData.is_already_parsed(log_files):
                self.match_and_dispatch_backup_files(folder_path, log_files)
        pass

    def match_and_dispatch_backup_files(self, folder_path, log_file_name):
        for regex in self.regex_internal_errors_mw_int:
            if regex.search(log_file_name):
                self.in_memory_logs.errors_int_mw_counter = self.count_errors(os.path.join(folder_path,log_file_name))
                return True


        for regex in self.regex_errors_mw_int:
            if regex.search(log_file_name):
                self.in_memory_logs.errors_mw_counter=self.count_errors(os.path.join(folder_path,log_file_name))
                return True

    def count_errors(self, file):
        counter=0
        with open(file, "r") as f:
            for x in f:
                x = x.rstrip()
                if not x: continue
                r = re.match(r'\[(?P<level>\w+)\]\s+(?P<date>\d{4}-\d{2}-\d{2})T(?P<time>\d{2}:\d{2}:\d{2})', x.strip())
                if r:
                    if r.group('level') in logs['log_level'][0:4]:

                        print r.group('level'), r.group('date'), r.group('time')
                        counter += 1
        return counter
                #for i in x.split("|"):
                 #   if not i: continue
