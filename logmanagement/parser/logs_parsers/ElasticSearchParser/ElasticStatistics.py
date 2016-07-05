__author__ = 'charls'

from ..TomcatParser.TomcatStatistics import TomcatStatistics
from logmanagement.parser.logs_parsers.ElasticSearchParser.LogsParserElasticSearch import LogsParserElasticSearch
from datetime import date,timedelta

class ElasticStatistics(TomcatStatistics):

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.parser = LogsParserElasticSearch()
        self.logs = self.parser.folders_iteration(self.start_date, self.end_date)


    def count_logs_by_log_level(self):
        return TomcatStatistics.count_logs_by_log_level(self)

    def get_dates_between(self):
        d1 = date(int(self.start_date.split("-")[0]), int(self.start_date.split("-")[1]),
                  int(self.start_date.split("-")[2]))
        d2 = date(int(self.end_date.split("-")[0]), int(self.end_date.split("-")[1]), int(self.end_date.split("-")[2]))
        dd = [str((d1 + timedelta(days=x))) for x in range((d2 - d1).days + 1)]
        return dd
