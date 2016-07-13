__author__ = 'charls'

from django import template
import datetime
import glob,os,re
from logmanagement.parser.InputsHandler import InputsHandler
register = template.Library()

@register.simple_tag(takes_context=True)
def get_monit_logs(context,folder,file='couchbase*-status*.txt'):
    file_handler = InputsHandler()
    file_handler.set_path_for_filesystem(subfolder="monit")
    newest = max(glob.iglob(file_handler.path_for_filesystem+os.sep+folder+os.sep+file), key=os.path.getctime)
    status = parse_file(newest)
    status['node1'] = newest
    return status


def parse_file(file):
    dict = {}
    key = ""

    with open(file, "r") as f:
        for x in f:
            x = x.rstrip().strip()
            if not x: continue
            x=x.replace(r'\d\;\d+m', "")
            r = re.match(r'Network\s+\'(?P<interface>.+)\'', x)
            if r:
                key='net'
                dict[key]={}
                dict[key]['interface']=r.group('interface')
                continue
            r = re.match(r'Process\s+\'(?P<process>.+)\'', x)
            if r:
                if 'process' in dict:
                    key='process1'
                else:
                    key='process'
                dict[key]={}
                dict[key]['process_name']=r.group('process')
                continue
            r = re.match(r'Filesystem\s+\'(?P<name>.+)\'', x)
            if r:
                key='file_system'
                dict[key]={}
                dict[key]['file_system_name']=r.group('name')
                continue
            r = re.match(r'File\s+\'(?P<name>.+)\'', x)
            if r:
                if 'file' in dict:
                    key = 'file1'
                else:
                    key='file'
                dict[key]={}
                dict[key]['file_name']=r.group('name')
                continue
            r = re.match(r'Program \'couchbase_logs_size\'', x)
            if r:
                key='couch_logs'
                dict[key]={}
                dict[key]['couch_name']='couchbase_logs_size'
                continue
            r = re.match(r'Program \'couchbase_data_size\'', x)
            if r:
                key='couch_data'
                dict[key] = {}
                dict[key]['couch_name']='couchbase_data_size'
                continue
            r = re.match(r'Program \'elastic_logs_size\'', x)
            if r:
                key='elastic_logs_size'
                dict[key] = {}
                dict[key]['couch_name']='elastic_logs_size'
                continue
            r = re.match(r'Program \'tomcat_logs_size\'', x)
            if r:
                key='tomcat_logs_size'
                dict[key] = {}
                dict[key]['tomcat_name']='tomcat_logs_size'
                continue
            r = re.match(r'Program \'vertx_logs_size\'', x)
            if r:
                key='vertx_logs_size'
                dict[key] = {}
                dict[key]['vertx_name']='vertx_logs_size'
                continue
            r = re.match(r'System \'(?P<system>.+)\'', x)
            if r:
                key='system'
                dict[key]={}
                dict[key]['system_name']=r.group('system')
                continue
            if key:
                try:
                    key_value=x.split(re.findall(r' {2,}',x)[0])
                    key_value[0]=key_value[0].replace(" ","_")
                    dict[key][key_value[0]]=key_value[1]
                except Exception as ex:
                    print ex


    return dict
