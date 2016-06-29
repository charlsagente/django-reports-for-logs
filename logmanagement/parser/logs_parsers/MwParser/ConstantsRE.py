__author__ = 'charls'
import re
from logmanagement.parser.LogsDictionary import *

REGEX_INTERNAL_ERRORS_MW_INT = [re.compile(p) for p in FILES_DICTIONARY[INTERNAL_MW_INT]]
REGEX_ERRORS_MW_INT = [re.compile(p) for p in FILES_DICTIONARY[INTERNAL_MW]]
REGEX_STRUCTURE_ERRORS_MW_INT = [re.compile(p) for p in FILES_DICTIONARY[STRUCTURE_MW]]
REGEX_SNDRCV_MSGS = [re.compile(p) for p in FILES_DICTIONARY[SNDRCVMSG]]
REGEX_LOG_LEVEL_TIMESTAMP = re.compile(
    r'\[(?P<level>\w+)\]\s+(?P<date>\d{4}-\d{2}-\d{2})T(?P<time>\d{2}:\d{2}:\d{2})')
REGEX_ADDRESS_RESPONSE = re.compile(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')
