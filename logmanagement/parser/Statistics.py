__author__ = 'charls'
from LogsParser import LogsParser
from LogsDictionary import INTERNAL_MW, INTERNAL_MW_INT, SNDRCVMSG


class Statistics:

    def __init__(self):
        parser= LogsParser()
        self.logs=parser.parse_backup_iteration()

    def count_logs_by_log_level(self):

        #for key, value in self.logs[INTERNAL_MW].iteritems():

            #print key,value
        return self.logs