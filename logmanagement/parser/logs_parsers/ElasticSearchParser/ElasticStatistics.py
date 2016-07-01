__author__ = 'charls'

from ..TomcatParser.TomcatStatistics import TomcatStatistics
from logmanagement.parser.logs_parsers.ElasticSearchParser.LogsParserElasticSearch import LogsParserElasticSearch


class ElasticStatistics(TomcatStatistics):

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.parser = LogsParserElasticSearch()
        self.logs = self.parser.folders_iteration(self.start_date, self.end_date)


    def count_logs_by_log_level(self):
        return TomcatStatistics.count_logs_by_log_level(self)

    def get_dates_between(self):
        return TomcatStatistics.get_dates_between(self)