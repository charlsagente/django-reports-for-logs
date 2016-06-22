# -*- coding: utf-8 -*-

__author__ = 'charls'
import os
import re
import copy

from InputsHandler import InputsHandler
from Logs import Logs
from LogsDictionary import *
from logmanagement.models import DateFile
from ConstantsRE import *

class LogsParser:
    def __init__(self):
        self.__inputData = InputsHandler()
        self.in_memory_logs = Logs()

    def get_Inputs_Handler(self):
        return self.__inputData

    def parse_backup_iteration(self, start_date, end_date):
        """
        Este método se debe invocar en la clase Statistics para inicializar todo el proceso.
        :param subfolder: Se envía el nombre de la subcarpeta en la que están los .log
        :return: Una clase diccionario con los datos parseados.
        """
        try:
            mw_backup_folder_path = os.path.join(self.__inputData.path_for_filesystem,
                                                 folders['middleware_backups_folder'])

            log_files = DateFile.objects.filter(fecha__gte=start_date).filter(fecha__lte=end_date) \
                .order_by('archivo').values('archivo').distinct()
            already_parsed_files = [f.archivo for f in DateFile.objects.all().order_by('archivo')]
        except Exception as ex:
            self.__inputData.log("Excepcion con lectura de la BD" + ex)

        self.__inputData.log("Leyendo mensajes")
        for entry in log_files:
            self.match_and_dispatch_backup_files(mw_backup_folder_path, entry['archivo'])

        for log_files in os.listdir(mw_backup_folder_path):
            if log_files not in already_parsed_files:
                self.match_and_dispatch_backup_files(mw_backup_folder_path, log_files)

        mw_folder_path = os.path.join(self.__inputData.path_for_filesystem, folders['middleware_folder'])
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
        for regex in regex_internal_errors_mw_int:
            if regex.search(log_file_name):
                self.parse_errors(os.path.join(folder_path, log_file_name), INTERNAL_MW_INT)
                self.iterate_file_continuous_lines(os.path.join(folder_path, log_file_name),
                                                   logs['log_level'][0],
                                                   returning_function=self.parse_int_mw_errors)
                return True

        for regex in regex_errors_mw_int:
            if regex.search(log_file_name):
                self.parse_errors(os.path.join(folder_path, log_file_name), INTERNAL_MW)
                return True

        for regex in regex_structure_errors_mw_int:
            if regex.search(log_file_name):
                self.iterate_file_continuous_lines(os.path.join(folder_path, log_file_name),
                                                   logs['log_level'][1],
                                                   returning_function=self.parse_and_count_complete_line)
                return True

        for regex in regex_sndrcv_msgs:
            if regex.search(log_file_name):
                self.iterate_file_continuous_lines(os.path.join(folder_path, log_file_name),
                                                   logs['log_level'][6],
                                                   returning_function=self.parse_sndrcv_complete_line)
                return True

        return False

    def parse_errors(self, file, log_type):

        with open(file, "r") as f:
            for x in f:
                x = x.rstrip()
                if not x: continue
                r = re.match(regex_log_level_timestamp, x.strip())
                if r and r.group('level') in logs['log_level'][0:4]:
                    print r.group('level'), r.group('date'), r.group('time')
                    self.in_memory_logs.add(log_type, r.group('date'), file.split(os.sep)[-1])
                    # self.__inputData.already_parsed(file.split(os.sep)[-1])

    def iterate_file_continuous_lines(self, file, log_level, returning_function):
        """

        :param file:
        :return:
        """
        continuous_line = False
        temp_line = ""
        line_number = 0
        with open(file, "r") as f:
            for x in f:
                line_number += 1
                x = x.rstrip()
                if not x: continue
                r = re.match(regex_log_level_timestamp, x.strip())
                if r and r.group('level') == log_level:
                    if continuous_line:
                        continuous_line = False
                        returning_function({'line': temp_line, 'file': file, 'line_number': line_number,
                                            'log_level':log_level})
                    if len(x.split('|')) >= 8:
                        continuous_line = False
                        returning_function({'line': x.strip(), 'file': file, 'line_number': line_number,
                                            'log_level':log_level})
                    else:
                        continuous_line = True
                        temp_line = x
                elif (continuous_line):
                    temp_line += " " + x
                else:
                    pass

    def parse_sndrcv_complete_line(self, dict):
        """

        :param line:
        :return:
        """
        separated_line = dict['line'].split('|')
        r = re.match(regex_log_level_timestamp, separated_line[0].strip())
        date = r.group("date")

        device_type = separated_line[1].strip()
        snd_or_rcv = separated_line[3].strip()
        address_response = separated_line[7].strip()
        execution_time = long(separated_line[6].strip())

        if (dict['line_number'] >= 1000 and dict['file'].split(os.sep)[
            -1] == 'PT-SndRcvMsg-Middleware-05-28-2016-3.log'):
            pass

        if snd_or_rcv in ['SNDSS', 'RCVSS']:
            if re.match(regex_address_response, address_response):
                self.in_memory_logs.addRcvSnd(date, device_type, snd_or_rcv, address_response, execution_time,
                                              dict['file'],
                                              dict['line_number'])
            else:
                pass

    def parse_and_count_complete_line(self, dict):
        separated_line = dict['line'].split('|')
        r = re.match(regex_log_level_timestamp, separated_line[0].strip())
        date = r.group("date")
        device_type = separated_line[1].strip()

        self.in_memory_logs.add_structure_counter(r.group('level'), device_type, date)


    def parse_int_mw_errors(self,dict):
        if len(dict['line'].split('|'))>=8:
            separated_line = dict['line'].split('|')
            device_type = separated_line[1].strip()
            r = re.match(regex_log_level_timestamp, separated_line[0].strip())
            date = r.group("date")


            if r and r.group('level') in logs['log_level'][0:4]:
                print r.group('level'), r.group('date'), r.group('time')
                self.in_memory_logs.add(log_type, r.group('date'), file.split(os.sep)[-1])

