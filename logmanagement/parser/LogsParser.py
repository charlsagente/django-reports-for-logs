__author__ = 'charls'
import os
import re
from InputsHandler import InputsHandler
from Logs import Logs
from LogsDictionary import dictionary, folders,logs,INTERNAL_MW,INTERNAL_MW_INT,SNDRCVMSG


class LogsParser:

    def __init__(self):
        self.__inputData = InputsHandler()
        self.regex_internal_errors_mw_int = [re.compile(p) for p in dictionary[INTERNAL_MW_INT]]
        self.regex_errors_mw_int = [re.compile(p) for p in dictionary[INTERNAL_MW]]
        self.regex_sndrcv_msgs=[re.compile(p) for p in dictionary[SNDRCVMSG]]
        self.regex_log_level_timestamp = re.compile(r'\[(?P<level>\w+)\]\s+(?P<date>\d{4}-\d{2}-\d{2})T(?P<time>\d{2}:\d{2}:\d{2})')
        self.regex_address_response = re.compile(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')
        self.in_memory_logs = Logs()



    def parse_backup_iteration(self, subfolder = folders['middleware_backups_folder']):
        folder_path = os.path.join(self.__inputData.path_for_filesystem, subfolder)
        for log_files in os.listdir(folder_path):
            if not self.__inputData.is_already_parsed(log_files):
                self.match_and_dispatch_backup_files(folder_path, log_files)
        return self.in_memory_logs

    def match_and_dispatch_backup_files(self, folder_path, log_file_name):
        for regex in self.regex_internal_errors_mw_int:
            if regex.search(log_file_name):
               self.parse_errors(os.path.join(folder_path,log_file_name),INTERNAL_MW_INT)
               return True

        for regex in self.regex_errors_mw_int:
            if regex.search(log_file_name):
               self.parse_errors(os.path.join(folder_path,log_file_name),INTERNAL_MW)
               return True

        for regex in self.regex_sndrcv_msgs:
            if regex.search(log_file_name):
                self.parse_sndrcv(os.path.join(folder_path,log_file_name))
                return True

    def parse_errors(self, file,log_type):

        with open(file, "r") as f:
            for x in f:
                x = x.rstrip()
                if not x: continue
                r = re.match(self.regex_log_level_timestamp, x.strip())
                if r and r.group('level') in logs['log_level'][0:4]:
                    print r.group('level'), r.group('date'), r.group('time')
                    self.in_memory_logs.add(log_type,r.group('date'))
        self.__inputData.already_parsed(file.split(os.sep)[-1])
                #for i in x.split("|"):
                 #   if not i: continue

    def parse_sndrcv(self,file):
        """

        :param file:
        :return:
        """
        continuous_line=False
        temp_line=""
        with open(file, "r") as f:
            for x in f:
                x = x.rstrip()
                if not x: continue
                r = re.match(self.regex_log_level_timestamp, x.strip())
                if r and  r.group('level') == logs['log_level'][6]:
                        if continuous_line:
                            continuous_line=False
                            self.parse_sndrcv_complete_line(temp_line)
                        if len(x.split('|'))>=8:
                            continuous_line=False
                            self.parse_sndrcv_complete_line(x.strip())
                        else:
                            continuous_line = True
                            temp_line=x
                elif(continuous_line):
                    temp_line += " " + x
                else:
                    pass

    def parse_sndrcv_complete_line(self, line):
        """

        :param line:
        :return:
        """
        separated_line=line.split('|')
        r = re.match(self.regex_log_level_timestamp, separated_line[0].strip())
        date=r.group("date")

        device_type=separated_line[1].strip()
        snd_or_rcv=separated_line[3].strip()
        address_response=separated_line[7].strip()
        execution_time=long(separated_line[6].strip())

        if snd_or_rcv in ['SNDSS','RCVSS']:
            if re.match(self.regex_address_response, address_response):
                self.in_memory_logs.addRcvSnd(date,device_type,snd_or_rcv,address_response,execution_time)
            else:
                pass

