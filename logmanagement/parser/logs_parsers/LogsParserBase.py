__author__ = 'charls'

import re

from logmanagement.parser.logs_parsers.MwParser.ConstantsRE import REGEX_LOG_LEVEL_TIMESTAMP
from logmanagement.parser.logs_parsers.TomcatParser.ConstantsRE import REGEX_TOMCAT_LOG_LEVELS

class LogsParserBase:



    def iterate_file_continuous_lines(self, file, log_level, *args, **kwargs):
        """
        Function to iterate a file and make the entire line in case exists break lines in log files
        :param file: Complete path of the file to parse
        :param log_level: Array of one or more log levels to parse
        :param *args: extra arguments
        :param **kwargs: Always send 'returning_function' inside **kwargs
        :return: Calls the returning_function and sends each complete line from the file
        """
        continuous_line = False
        temp_line = ""
        line_number = 0
        temp_line_number = 0
        with open(file, "r") as f:
            for x in f:
                line_number += 1

                x = x.rstrip()
                if not x: continue
                r = re.match(REGEX_LOG_LEVEL_TIMESTAMP, x.strip())
                if r and r.group('level') in log_level:
                    if continuous_line:
                        continuous_line = False
                        kwargs['returning_function']({'line': temp_line, 'file': file, 'line_number': temp_line_number},
                                                     *args)
                    if len(x.split('|')) >= 8:
                        continuous_line = False
                        kwargs['returning_function']({'line': x.strip(), 'file': file, 'line_number': line_number},
                                                     *args)
                    else:
                        continuous_line = True
                        temp_line = x
                        temp_line_number = line_number

                elif continuous_line:
                    temp_line += " " + x

        try:
            if not x:
                kwargs['returning_function']({'line': temp_line, 'file': file, 'line_number': line_number,
                                              'log_level': log_level}, *args)
        except UnboundLocalError as ex:
            print ex


    def iterate_file_and_return_log_types(self,file,*args,**kwargs):

        line_number = 0
        with open(file, "r") as f:
            for x in f:
                line_number += 1
                x = x.rstrip()
                if not x: continue
                for log_level in REGEX_TOMCAT_LOG_LEVELS:
                    r = log_level.search(x.strip())
                    if r:
                        kwargs['returning_function'](x.strip(),r.group('log_level'),args[0],line_number,file)

