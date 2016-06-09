__author__ = 'charls'
from LogsParser import LogsParser
from LogsDictionary import INTERNAL_MW, INTERNAL_MW_INT, SNDRCVMSG
from datetime import date, timedelta

class Statistics:

    def __init__(self):
        parser= LogsParser()
        self.logs=parser.parse_backup_iteration()


    def count_logs_by_log_level(self,start_date,end_date):

        counted_logs={INTERNAL_MW:0,
                      INTERNAL_MW_INT:0,
                      SNDRCVMSG:{'W': {}, 'I': {}, 'A': {}}}
        dates_between= self.get_dates_between(start_date,end_date)

        for key, value in self.logs[INTERNAL_MW].iteritems():
            if key in dates_between:
                print key,value
                counted_logs[INTERNAL_MW]+=value


        return self.logs

    def get_dates_between(self,start_date,end_date):
        d1= date(int(start_date.split("-")[0]),int(start_date.split("-")[1]),int(start_date.split("-")[2]))
        d2=date(int(end_date.split("-")[0]),int(end_date.split("-")[1]),int(end_date.split("-")[2]))
        dd = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
        return dd
