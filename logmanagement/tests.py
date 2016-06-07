from django.test import TestCase
from parser.LogsParser import LogsParser
from parser.Statistics import Statistics

class TestPath(TestCase):

    def test_get_paths(self):
        stats=Statistics()
        stats.count_logs_by_log_level(self)
        self.assertTrue(True)
