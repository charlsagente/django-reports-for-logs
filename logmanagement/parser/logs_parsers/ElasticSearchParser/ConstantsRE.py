__author__ = 'charls'
from logmanagement.parser.LogsDictionary import LOG_LEVELS
import re

REGEX_ELASTIC_TIMESTAMP = re.compile(
    r'(?P<date>\d{4}-\d{2}-\d{2})')

REGEX_ELASTIC_LOG_LEVELS =\
    [re.compile(r'(?P<log_level>'+p+')') for p in LOG_LEVELS['tomcat_levels']]
