__author__ = 'charls'

from datetime import datetime, timedelta
from logmanagement.parser.LogsDictionary import TOMCAT_LOGS,LOG_LEVELS
from logmanagement.parser.logs_parsers.TomcatParser.LogsParserTomcat import LogsParserTomcat
from datetime import date


class TomcatStatistics:
    def __init__(self,start_date,end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.parser = LogsParserTomcat()
        self.logs = self.parser.folders_iteration(self.start_date, self.end_date)

    def count_logs_by_log_level(self):
        dates_between=self.get_dates_between()
        keys_to_delete=[]
        if self.logs:
            for log_level in self.logs[TOMCAT_LOGS]:
                for key, value in self.logs[TOMCAT_LOGS][log_level].iteritems():
                    if key not in dates_between and key not in keys_to_delete:
                        keys_to_delete.append(key)

            for log_level in self.logs[TOMCAT_LOGS]:
                for key in keys_to_delete:
                    if key in self.logs[TOMCAT_LOGS][log_level]:
                        del self.logs[TOMCAT_LOGS][log_level][key]

            keys_to_delete=[]

            for log_level in self.logs['files']:
                for key, value in self.logs['files'][log_level].iteritems():
                    if key not in dates_between and key not in keys_to_delete:
                        keys_to_delete.append(key)
            for log_level in self.logs['files']:
                for key in keys_to_delete:
                    if key in self.logs['files'][log_level]:
                        del self.logs['files'][log_level][key]

        return self.logs

    def get_dates_between(self):
        d1 = date(int(self.start_date.split("-")[0]), int(self.start_date.split("-")[1]),
                  int(self.start_date.split("-")[2]))
        d2 = date(int(self.end_date.split("-")[0]), int(self.end_date.split("-")[1]), int(self.end_date.split("-")[2]))
        dd = [str((d1 + timedelta(days=x)).strftime('%d-%b-%Y')) for x in range((d2 - d1).days + 1)]
        return dd

