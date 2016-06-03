from django.test import TestCase
from parser.LogsParser import LogsParser


class TestPath(TestCase):

    def test_get_paths(self):
        parser= LogsParser()
        parser.parse_backup_iteration()
        self.assertTrue(True)
