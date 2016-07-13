__author__ = 'charls'

from ..MwParser.MwStatistics import MwStatistics
from LogsParserMwRest import LogsParserMWRest

class MwRestStatistics(MwStatistics):
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.parser = LogsParserMWRest()
        self.logs = self.parser.folders_iteration(self.start_date, self.end_date)
        self.index_files()


    def count_logs_by_log_level(self):
        return MwStatistics.count_logs_by_log_level(self)

    def get_dates_between(self):
        return MwStatistics.get_dates_between(self)

    def index_files(self):
        #MwStatistics.index_files(self)
        pass
