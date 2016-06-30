__author__ = 'charls'

from ..MwParser.LogsParserMW import LogsParserMW
from logmanagement.parser.LogsDictionary import *
from logmanagement.models import DateFileRest

import os
import copy

class LogsParserMWRest(LogsParserMW):
    def __init__(self):
        LogsParserMW.__init__(self)

    def iterate_file_continuous_lines(self, file, log_level, *args, **kwargs):
        LogsParserMW.iterate_file_continuous_lines(self, file, log_level, *args, **kwargs)

    def folders_iteration(self, start_date, end_date):
        try:
            mw_backup_folder_path = os.path.join(self.inputData.path_for_filesystem,
                                                 MAIN_FOLDERS['rest_folder_backup'])

            log_files = DateFileRest.objects.filter(fecha__gte=start_date).filter(fecha__lte=end_date) \
                .order_by('archivo').values('archivo').distinct()
            already_parsed_files = [f.archivo for f in DateFileRest.objects.all().order_by('archivo')]
        except Exception as ex:
            self.inputData.log("Excepcion con lectura de la BD" + ex)

        for entry in log_files:
            self.match_and_dispatch_backup_files(mw_backup_folder_path, entry['archivo'])

        for log_files in os.listdir(mw_backup_folder_path):
            if log_files not in already_parsed_files:
                self.match_and_dispatch_backup_files(mw_backup_folder_path, log_files)

        mw_folder_path = os.path.join(self.inputData.path_for_filesystem, MAIN_FOLDERS['rest_folder'])
        for log_files in os.listdir(mw_folder_path):
            self.match_and_dispatch_backup_files(mw_folder_path, log_files)

        return copy.deepcopy(self.in_memory_logs.LogData)


    def match_and_dispatch_backup_files(self, folder_path, log_file_name):
        return LogsParserMW.match_and_dispatch_backup_files(self, folder_path, log_file_name)

    def parse_sndrcv_complete_line(self, dict, *args):
        LogsParserMW.parse_sndrcv_complete_line(self, dict, *args)

    def parse_and_count_complete_line(self, dict, *args):
        LogsParserMW.parse_and_count_complete_line(self, dict, *args)

    def parse_int_mw_errors(self, dict, *args):
        LogsParserMW.parse_int_mw_errors(self, dict, *args)

    def get_Inputs_Handler(self):
        return LogsParserMW.get_Inputs_Handler(self)