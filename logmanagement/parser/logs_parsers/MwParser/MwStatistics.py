__author__ = 'charls'
from datetime import date, timedelta
import os

from logmanagement.parser.logs_parsers.MwParser.LogsParserMW import LogsParserMW
from logmanagement.parser.LogsDictionary import *
from logmanagement.models import DateFile


class MwStatistics:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.parser = LogsParserMW()
        self.logs = self.parser.folders_iteration(self.start_date, self.end_date)
        self.index_files()

    def count_logs_by_log_level(self):

        counted_logs = {
            COUNTERS_ERRORS_EACH_FILE: {'W': {}, 'I': {}, 'A': {}},
            ERRORS_INTERNAL_PT:{},
            INTERNAL_MW: 0,
            INTERNAL_MW_INT: 0,
            STRUCTURE_MW: {'W': 0, 'I': 0, 'A': 0},
            PATH_LOG_ERRORS: {'W': [], 'I': [], 'A': []},
            SNDRCVMSG: {'W': {'success_attended': 0,
                              'avg_time': 0,
                              'failed_attended': 0,
                              'sum_for_avg': []}, 'I': {'success_attended': 0,
                                                        'avg_time': 0,
                                                        'failed_attended': 0,
                                                        'sum_for_avg': []}, 'A': {'success_attended': 0,
                                                                                  'avg_time': 0,
                                                                                  'failed_attended': 0,
                                                                                  'sum_for_avg': []}}}

        dates_between = self.get_dates_between()

        if self.logs:
            if ERRORS_INTERNAL_PT in self.logs:
                counted_logs[ERRORS_INTERNAL_PT]=self.logs[ERRORS_INTERNAL_PT]

            if INTERNAL_MW in self.logs:
                for key, value in self.logs[INTERNAL_MW].iteritems():
                    if key in dates_between:
                        print "INTERNAL_MW ", key, value
                        counted_logs[INTERNAL_MW] += value

            if STRUCTURE_MW in self.logs:
                for device in self.logs[STRUCTURE_MW]:
                    for date in self.logs[STRUCTURE_MW][device]:
                        if date in dates_between:
                            counted_logs[STRUCTURE_MW][device] += self.logs[STRUCTURE_MW][device][date]

            if INTERNAL_MW_INT in self.logs:
                for key, value in self.logs[INTERNAL_MW_INT].iteritems():
                    if key in dates_between:
                        counted_logs[INTERNAL_MW_INT] += value
                        print "INTERNAL_MW_INT", key, value

            if SNDRCVMSG in self.logs:
                for device in self.logs[SNDRCVMSG]:
                    for address_response in self.logs[SNDRCVMSG][device]:
                        values = self.logs[SNDRCVMSG][device][address_response]
                        if values['date'] in dates_between:
                            if values['response']:
                                counted_logs[SNDRCVMSG][device]['success_attended'] += 1
                                counted_logs[SNDRCVMSG][device]['sum_for_avg'].append(values['time_stamp'])
                            else:
                                counted_logs[SNDRCVMSG][device]['failed_attended'] += 1
                                if not values['file'] in counted_logs[PATH_LOG_ERRORS][device]:
                                    counted_logs[PATH_LOG_ERRORS][device].append(values['file'])
                                    counted_logs[COUNTERS_ERRORS_EACH_FILE][device][values['file']] = {
                                        'line_counters': 1,
                                        'lines': [values['line_number']]
                                    }

                                else:
                                    counted_logs[COUNTERS_ERRORS_EACH_FILE][device][values['file']][
                                        'line_counters'] += 1
                                    counted_logs[COUNTERS_ERRORS_EACH_FILE][device][values['file']]['lines'].append(
                                        values['line_number'])



                    if len(counted_logs[SNDRCVMSG][device]['sum_for_avg']) > 0:
                        counted_logs[SNDRCVMSG][device]['avg_time'] = (
                        sum(counted_logs[SNDRCVMSG][device]['sum_for_avg']) /
                        len(counted_logs[SNDRCVMSG][device]['sum_for_avg']))
                        counted_logs[SNDRCVMSG][device]['avg_time'] = round(counted_logs[SNDRCVMSG][device]['avg_time'],
                                                                            3)
                        del counted_logs[SNDRCVMSG][device]['sum_for_avg'][:]
                    del counted_logs[SNDRCVMSG][device]['sum_for_avg']

        return counted_logs

    def get_dates_between(self):
        d1 = date(int(self.start_date.split("-")[0]), int(self.start_date.split("-")[1]),
                  int(self.start_date.split("-")[2]))
        d2 = date(int(self.end_date.split("-")[0]), int(self.end_date.split("-")[1]), int(self.end_date.split("-")[2]))
        dd = [str(d1 + timedelta(days=x)) for x in range((d2 - d1).days + 1)]
        return dd

    def index_files(self):
        if self.logs:
            files = set()

            for device in self.logs[SNDRCVMSG]:
                for address_response in self.logs[SNDRCVMSG][device]:
                    values = self.logs[SNDRCVMSG][device][address_response]
                    if not values['date'] + "-" + values['file'].split(os.sep)[-1] in files \
                            and values['file'].split(os.sep)[-2] != "mw":
                        try:
                            DateFile.objects.create(
                                fecha_archivo=values['date'] + "-" + values['file'].split(os.sep)[-1],
                                fecha=values['date'],
                                archivo=values['file'].split(os.sep)[-1]).save()
                        except Exception as ex:
                            print "MwStatistics.index_files ", ex
                            self.parser.get_Inputs_Handler().log("MwStatistics.index_files " + ex.message)
                        finally:
                            files.add(values['date'] + "-" + values['file'].split(os.sep)[-1])
