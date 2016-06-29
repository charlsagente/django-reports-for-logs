# -*- coding: utf-8 -*-

__author__ = 'charls'
from logmanagement.parser.LogsDictionary import TOMCAT_LOGS,LOG_LEVELS
import os

class Logs:
    def __init__(self):
        self.LogData = {TOMCAT_LOGS: {},
                        'files': {},
                        'tomcat':{}}
        for log in LOG_LEVELS['tomcat_levels']:
            self.LogData[TOMCAT_LOGS][log] = {}

    def add_error_log(self, log_level, date, *args):
        """

        :param log_level: Definidos en LogsDictionary.log_levels['tomcat_levels']
        :param date: fecha extraída en el parser
        :param args: args[0] nombre del archivo, args[1] numero de línea
        :return: Modifica self.LogData con los datos correspondientes.
        """
        if date in self.LogData[TOMCAT_LOGS][log_level]:
            self.LogData[TOMCAT_LOGS][log_level][date] += 1
        else:
            self.LogData[TOMCAT_LOGS][log_level][date] = 1

        if log_level not in self.LogData['files']:
            self.LogData['files'][log_level] = {}
        if date not in self.LogData['files'][log_level]:
            self.LogData['files'][log_level][date] = {}
        semipath = args[2].split(os.sep)[-2]+os.sep+args[0]
        if semipath not in self.LogData['files'][log_level][date]:
            self.LogData['files'][log_level][date][semipath]=[]
            self.LogData['files'][log_level][date][semipath].append(args[1])
        else:
            self.LogData['files'][log_level][date][semipath].append(args[1])

    def add_counted_errors_for_tomcat(self, log_level, *args):
        semi_path=args[2].split(os.sep)[-2]+os.sep+args[0]
        if semi_path not in self.LogData['tomcat']:
            self.LogData['tomcat'][semi_path] = {}
        if log_level in self.LogData['tomcat'][semi_path]:
            self.LogData['tomcat'][semi_path][log_level].append(args[1])
        else:
            self.LogData['tomcat'][semi_path][log_level] = []
            self.LogData['tomcat'][semi_path][log_level].append(args[1])

