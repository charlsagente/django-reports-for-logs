__author__ = 'charls'
import re
from logmanagement.parser.LogsDictionary import LOG_LEVELS

REGEX_TOMCAT_TIMESTAMP = re.compile(
    r'(?P<date>\d{2}-\w{3}-\d{4})')

REGEX_TOMCAT_LOG_LEVELS=[re.compile(r'(?P<log_level>'+p+')') for p in LOG_LEVELS['tomcat_levels']]
