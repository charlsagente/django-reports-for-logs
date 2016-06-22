__author__ = 'charls'
import re
from LogsDictionary import *

regex_internal_errors_mw_int = [re.compile(p) for p in dictionary[INTERNAL_MW_INT]]
regex_errors_mw_int = [re.compile(p) for p in dictionary[INTERNAL_MW]]
regex_structure_errors_mw_int = [re.compile(p) for p in dictionary[STRUCTURE_MW]]
regex_sndrcv_msgs = [re.compile(p) for p in dictionary[SNDRCVMSG]]
regex_log_level_timestamp = re.compile(
    r'\[(?P<level>\w+)\]\s+(?P<date>\d{4}-\d{2}-\d{2})T(?P<time>\d{2}:\d{2}:\d{2})')
regex_address_response = re.compile(r'\w{8}-\w{4}-\w{4}-\w{4}-\w{12}')
