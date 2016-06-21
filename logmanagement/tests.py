from django.test import TestCase
from parser.LogsParser import LogsParser
from parser.Statistics import Statistics
from models import DateFile
import datetime
import re


class TestPath(TestCase):

    def test_get_paths(self):
       text="e6d3acff-d193-45db-9c0d-48439072bde7-SS"
       regex_address_response = re.compile(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')
       if re.match(regex_address_response, text):
          pass


