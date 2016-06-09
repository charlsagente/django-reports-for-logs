__author__ = 'charls'
from LogsDictionary import INTERNAL_MW, INTERNAL_MW_INT, SNDRCVMSG
from DynamoDB import DynamoBD
import time

class Logs:
    def __init__(self):
        self.LogData = {
            INTERNAL_MW_INT: {},
            INTERNAL_MW: {},
            SNDRCVMSG: {'W': {}, 'I': {}, 'A': {}}
        }
        self.__addresses = set()
        self.DynamoDb = DynamoBD()

    def add(self, level, date):
        if date in self.LogData[level]:
            self.LogData[level][date] += 1
        else:
            self.LogData[level][date] = 1

    def addRcvSnd(self, date, device_type, snd_or_rcv, address_response, execution_time):

        if address_response in self.LogData[SNDRCVMSG][device_type.upper()] and not address_response in \
                self.__addresses:

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
            insert = {
                'execution_date_time': self.LogData[SNDRCVMSG][device_type.upper()][address_response]['id'],
                'date':self.LogData[SNDRCVMSG][device_type.upper()][address_response]['date'],
                'total_execution_time':str(self.LogData[SNDRCVMSG][device_type.upper()][address_response]['time_stamp']),
                'service_attended':self.LogData[SNDRCVMSG][device_type.upper()][address_response]['response'],
                'device_type':device_type
            }
            #self.DynamoDb.putItem(insert)
            #time.sleep(0.33)

        else:
            self.LogData[SNDRCVMSG][device_type.upper()][address_response] = {}
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['id'] = long(execution_time)
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['date'] = date
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['time_stamp'] = execution_time
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['response'] = False
            self.LogData[SNDRCVMSG][device_type.upper()][address_response]['snd_or_rcv'] = snd_or_rcv

    def __del__(self):
        pass
