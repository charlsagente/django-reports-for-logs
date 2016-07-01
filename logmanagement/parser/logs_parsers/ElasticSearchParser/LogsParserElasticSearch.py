__author__ = 'charls'

from ..TomcatParser.LogsParserTomcat import LogsParserTomcat
from logmanagement.parser.LogsDictionary import *


class LogsParserElasticSearch(LogsParserTomcat):

    def __init__(self):
        LogsParserTomcat.__init__(self)

    def iterate_file_and_return_log_types(self, file, *args, **kwargs):
        LogsParserTomcat.iterate_file_and_return_log_types(self, file, *args, **kwargs)

    def folders_iteration(self, start_date, end_date):
        return LogsParserTomcat.folders_iteration(self, start_date, end_date)

    def parse_and_count_errors(self, line, log_level, *args):
        LogsParserTomcat.parse_and_count_errors(self, line, log_level, *args)
