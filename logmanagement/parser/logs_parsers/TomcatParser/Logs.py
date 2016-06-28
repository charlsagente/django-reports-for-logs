# -*- coding: utf-8 -*-

__author__ = 'charls'
from logmanagement.parser.LogsDictionary import TOMCAT_LOGS,LOG_LEVELS

class Logs:
    def __init__(self):
        self.LogData = {TOMCAT_LOGS: {},
                        'files': {}}
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

        if args[0] not in self.LogData['files'][log_level][date]:
            self.LogData['files'][log_level][date][args[0]]=[]
            self.LogData['files'][log_level][date][args[0]].append(args[1])
        else:
            self.LogData['files'][log_level][date][args[0]].append(args[1])


