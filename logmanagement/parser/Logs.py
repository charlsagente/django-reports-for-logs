__author__ = 'charls'
from LogsDictionary import *
from DynamoDB import DynamoBD
import os


class Logs:
    def __init__(self):
        self.LogData = {
            INTERNAL_MW_INT: {},
            INTERNAL_MW: {},
            STRUCTURE_MW: {'W': {}, 'I': {}, 'A': {}},
            SNDRCVMSG: {'W': {}, 'I': {}, 'A': {}},
            ERRORS_INTERNAL_PT: {'W': [], 'I': [], 'A': []}

        }
        self.__addresses = set()

    def add(self, level, date, file_name):
        if date in self.LogData[level]:
            self.LogData[level][date] += 1
        else:
            self.LogData[level][date] = 1


    def add_mw_pt_internal_errors(self,dict):
        self.LogData[ERRORS_INTERNAL_PT][dict['device']].append(dict)


    def add_structure_counter(self,level,device,date):
        if date in self.LogData[STRUCTURE_MW][device]:
            self.LogData[STRUCTURE_MW][device][date]+=1
        else:
            self.LogData[STRUCTURE_MW][device][date]=1

    def addRcvSnd(self, date, device_type, snd_or_rcv, address_response, execution_time,file,line_number):

        if address_response in self.LogData[SNDRCVMSG][device_type.upper()]:
            if address_response not in self.__addresses:

                self.__addresses.add(address_response)
                last_send_or_receive=self.LogData[SNDRCVMSG][device_type.upper()][address_response]['snd_or_rcv']
                if last_send_or_receive=="RCVSS":
                    self.LogData[SNDRCVMSG][device_type.upper()][address_response]['time_stamp'] = (self.LogData[SNDRCVMSG][
                                                                                                    device_type.upper()][
                                                                                                    address_response][
                                                                                                    'time_stamp'] - execution_time) / 1e9
                elif last_send_or_receive=="SNDSS":
                    self.LogData[SNDRCVMSG][device_type.upper()][address_response]['time_stamp'] = (execution_time - self.LogData[SNDRCVMSG][
                                                                                                        device_type.upper()][
                                                                                                        address_response][
                                                                                                        'time_stamp'] ) / 1e9
                self.LogData[SNDRCVMSG][device_type.upper()][address_response]['response'] = True


        else:
            self.LogData[SNDRCVMSG][device_type.upper()][address_response] = {}
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['execution_date_time'] = long(execution_time)
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['date'] = date
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['time_stamp'] = execution_time
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['response'] = False
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['snd_or_rcv'] = snd_or_rcv
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['file'] = file.split(os.sep)[-2]+\
                                                                                     os.sep + file.split(os.sep)[-1]
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['line_number'] = line_number




    def __del__(self):
        pass
