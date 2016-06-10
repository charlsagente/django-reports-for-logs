from django.test import TestCase
from parser.LogsParser import LogsParser
from parser.Statistics import Statistics
from parser.DynamoDB import DynamoBD

class TestPath(TestCase):

    def test_get_paths(self):
        bd=DynamoBD()

        item={
            'execution_date_time': 2344433434342,
            'dia':True,
            'noche':False
        }
        try:
            print bd.putItem(item)
        except Exception as ex:
            print ex

        self.assertTrue(True)
