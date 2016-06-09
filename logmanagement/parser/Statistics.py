__author__ = 'charls'
from LogsParser import LogsParser
from LogsDictionary import INTERNAL_MW, INTERNAL_MW_INT, SNDRCVMSG
from datetime import date, timedelta


class Statistics:

    def __init__(self):
        parser= LogsParser()
        self.logs=parser.parse_backup_iteration()

    def count_logs_by_log_level(self, start_date, end_date):

        counted_logs = {INTERNAL_MW :0,
                      INTERNAL_MW_INT :0,
                      SNDRCVMSG:{'W': {'success_attended':0,
                                       'avg_time':0,
                                       'failed_attended':0,
                                       'sum_for_avg':[]}, 'I': {'success_attended':0,
                                                                'avg_time':0,
                                                                'failed_attended':0,
                                                                'sum_for_avg':[]}, 'A': {'success_attended':0,
                                                                                         'avg_time':0,
                                                                                         'failed_attended':0,
                                                                                         'sum_for_avg':[]}}}

        dates_between = self.get_dates_between(start_date,end_date)

        for key, value in self.logs[INTERNAL_MW].iteritems():
            if key in dates_between:
                print key, value
                counted_logs[INTERNAL_MW] += value

        for key, value in self.logs[INTERNAL_MW_INT].iteritems():
                if key in dates_between:
                    counted_logs[INTERNAL_MW_INT] += value
                    print key, value

        for device in self.logs[SNDRCVMSG]:
            for address_response in self.logs[SNDRCVMSG][device]:
                values = self.logs[SNDRCVMSG][device][address_response]
                if values['date'] in dates_between:
                    if values['response']:
                        counted_logs[SNDRCVMSG][device]['success_attended'] += 1
                        counted_logs[SNDRCVMSG][device]['sum_for_avg'].append(values['time_stamp'])
                    else:
                        counted_logs[SNDRCVMSG][device]['failed_attended'] += 1
            if len(counted_logs[SNDRCVMSG][device]['sum_for_avg']) > 0:
                counted_logs[SNDRCVMSG][device]['avg_time'] = (sum(counted_logs[SNDRCVMSG][device]['sum_for_avg']) /
                                                           len(counted_logs[SNDRCVMSG][device]['sum_for_avg']))
                counted_logs[SNDRCVMSG][device]['avg_time']=round(counted_logs[SNDRCVMSG][device]['avg_time'],2)
                del counted_logs[SNDRCVMSG][device]['sum_for_avg'][:]
            del counted_logs[SNDRCVMSG][device]['sum_for_avg']



        return counted_logs

    def get_dates_between(self,start_date, end_date):
        d1 = date(int(start_date.split("-")[0]),int(start_date.split("-")[1]),int(start_date.split("-")[2]))
        d2 = date(int(end_date.split("-")[0]),int(end_date.split("-")[1]),int(end_date.split("-")[2]))
        dd = [str(d1 + timedelta(days=x)) for x in range((d2-d1).days + 1)]
        return dd
