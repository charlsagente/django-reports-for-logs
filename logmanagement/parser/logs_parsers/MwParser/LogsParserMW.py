# -*- coding: utf-8 -*-

__author__ = 'charls'
import os
import copy

from logmanagement.parser.InputsHandler import InputsHandler
from logmanagement.parser.logs_parsers.MwParser.Logs import Logs
from logmanagement.models import DateFile
from logmanagement.parser.logs_parsers.MwParser.ConstantsRE import *
from logmanagement.parser.logs_parsers.LogsParserBase import LogsParserBase


class LogsParserMW(LogsParserBase):
    def __init__(self):
        self.inputData = InputsHandler()
        self.in_memory_logs = Logs()

    def iterate_file_continuous_lines(self, file, log_level, *args, **kwargs):
        LogsParserBase.iterate_file_continuous_lines(self, file, log_level, *args, **kwargs)

    def get_Inputs_Handler(self):
        return self.inputData

    def folders_iteration(self, start_date, end_date):
        """
        Este método se debe invocar en la clase MwStatistics para inicializar todo el proceso.
        :param subfolder: Se envía el nombre de la subcarpeta en la que están los .log
        :return: Una clase diccionario con los datos parseados.
        """
        try:
            mw_backup_folder_path = os.path.join(self.inputData.path_for_filesystem,
                                                 MAIN_FOLDERS['middleware_backups_folder'])

            log_files = DateFile.objects.filter(fecha__gte=start_date).filter(fecha__lte=end_date) \
                .order_by('archivo').values('archivo').distinct()
            already_parsed_files = [f.archivo for f in DateFile.objects.all().order_by('archivo')]
        except Exception as ex:
            self.inputData.log("Excepcion con lectura de la BD" + ex)

        self.inputData.log("Leyendo mensajes")
        for entry in log_files:
            self.match_and_dispatch_backup_files(mw_backup_folder_path, entry['archivo'])

        for log_files in os.listdir(mw_backup_folder_path):
            if log_files not in already_parsed_files:
                self.match_and_dispatch_backup_files(mw_backup_folder_path, log_files)

        mw_folder_path = os.path.join(self.inputData.path_for_filesystem, MAIN_FOLDERS['middleware_folder'])
        for log_files in os.listdir(mw_folder_path):
            self.match_and_dispatch_backup_files(mw_folder_path, log_files)

        return copy.deepcopy(self.in_memory_logs.LogData)

    def match_and_dispatch_backup_files(self, folder_path, log_file_name):
        """
        Se buscan todas las posibles expresiones regulares con los nombres de los archivos.
        :param folder_path:
        :param log_file_name:
        :return: True si se encuentra un archivo con una expresion regular, false si no
        """
        for regex in REGEX_INTERNAL_ERRORS_MW_INT:
            if regex.search(log_file_name):
                # self.parse_errors(os.path.join(folder_path, log_file_name), INTERNAL_MW_INT)
                self.iterate_file_continuous_lines(os.path.join(folder_path, log_file_name),
                                                   LOG_LEVELS['log_level'][0:4],
                                                   INTERNAL_MW_INT, returning_function=self.parse_int_mw_errors)
                return True

        for regex in REGEX_ERRORS_MW_INT:
            if regex.search(log_file_name):
                # self.parse_errors(os.path.join(folder_path, log_file_name), INTERNAL_MW)
                self.iterate_file_continuous_lines(os.path.join(folder_path, log_file_name),
                                                   LOG_LEVELS['log_level'][0:4],
                                                   INTERNAL_MW, returning_function=self.parse_int_mw_errors)
                return True

        for regex in REGEX_STRUCTURE_ERRORS_MW_INT:
            if regex.search(log_file_name):
                self.iterate_file_continuous_lines(os.path.join(folder_path, log_file_name),
                                                   LOG_LEVELS['log_level'][1],
                                                   returning_function=self.parse_and_count_complete_line)
                return True

        for regex in REGEX_SNDRCV_MSGS:
            if regex.search(log_file_name):
                self.iterate_file_continuous_lines(os.path.join(folder_path, log_file_name),
                                                   LOG_LEVELS['log_level'][6],
                                                   returning_function=self.parse_sndrcv_complete_line)
                return True

        return False


    def parse_sndrcv_complete_line(self, dict, *args):
        """

        :param line:
        :return:
        """
        separated_line = dict['line'].split('|')
        r = re.match(REGEX_LOG_LEVEL_TIMESTAMP, separated_line[0].strip())
        date = r.group("date")

        device_type = separated_line[1].strip()
        snd_or_rcv = separated_line[3].strip()
        address_response = separated_line[7].strip()
        execution_time = long(separated_line[6].strip())

        if (dict['line_number'] >= 1000 and dict['file'].split(os.sep)[
            -1] == 'PT-SndRcvMsg-Middleware-05-28-2016-3.log'):
            pass

        if snd_or_rcv in ['SNDSS', 'RCVSS']:
            if re.match(REGEX_ADDRESS_RESPONSE, address_response):
                self.in_memory_logs.addRcvSnd(date, device_type, snd_or_rcv, address_response, execution_time,
                                              dict['file'],
                                              dict['line_number'])
            else:
                pass

    def parse_and_count_complete_line(self, dict, *args):
        separated_line = dict['line'].split('|')
        r = re.match(REGEX_LOG_LEVEL_TIMESTAMP, separated_line[0].strip())
        date = r.group("date")
        device_type = separated_line[1].strip()

        self.in_memory_logs.add_structure_counter(r.group('level'), device_type, date)

    def parse_int_mw_errors(self, dict, *args):
        separated_line = dict['line'].split('|')
        r = re.match(REGEX_LOG_LEVEL_TIMESTAMP, separated_line[0].strip())
        if r and r.group('level') in LOG_LEVELS['log_level'][0:4]:
            print r.group('level'), r.group('date'), r.group('time')
            self.in_memory_logs.add(args[0], r.group('date'), dict['file'].split(os.sep)[-1])

        if len(dict['line'].split('|')) >= 8:
            dictionary = {}
            dictionary['date'] = r.group("date")
            dictionary['device'] = separated_line[1].strip()
            dictionary['error_type'] = r.group('level')
            dictionary['service_id']=separated_line[2]

            dictionary['class'] = separated_line[0].split(" ")[2]
            dictionary['file'] = dict['file'].split(os.sep)[-2] +\
                            os.sep + dict['file'].split(os.sep)[-1]

            self.in_memory_logs.add_mw_pt_internal_errors(dictionary)
