import re

from django.test import TestCase
from logmanagement.parser.logs_parsers.MwRest.MwRestStatistics import MwRestStatistics


class TestPath(TestCase):

    def test_get_paths(self):
        stats = MwRestStatistics("2016-05-01","2016-06-28")
        data=stats.count_logs_by_log_level()
        print data


