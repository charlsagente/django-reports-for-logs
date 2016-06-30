__author__ = 'charls'

INTERNAL_MW_INT = 'internal-errors-mw-int'
INTERNAL_MW = 'errors-mw-int'
STRUCTURE_MW = 'structure-mw'
SNDRCVMSG = 'sndrcvmsgs'
PATH_LOG_ERRORS='pathlogs'
COUNTERS_ERRORS_EACH_FILE='counter_errors_each_file'
ERRORS_INTERNAL_PT='pt-internal-errors'
TOMCAT_LOGS='tomcat_logs'

FILES_DICTIONARY = {
    INTERNAL_MW_INT: ['Integrator-Internal-SocieChat',
                      'PT-Internal-Middleware'],
    INTERNAL_MW: ['Integrator-Error-SocieChat',
                  'PT-Error-Middleware'],
    STRUCTURE_MW: ['PT-Structure-Middleware'],
    SNDRCVMSG: ['Integrator-SndRcvMsg-SocieChat', 'PT-SndRcvMsg-Middleware']
}

MAIN_FOLDERS = {
    'middleware_folder': 'mw',
    'middleware_backups_folder': 'mwbkup',
    'tomcat_folder':'tomcat',
    'rest_folder':'mwrest',
    'rest_folder_backup':'mwrestbkup'
}

LOG_LEVELS = {
    'log_level': ['INTERNAL', 'STRUCTURE', 'LOSTMSG', 'ERROR', 'WARN', 'FUNCTIONAL', 'SNDRCVMSG', 'INFO', 'DEBUG',
                  'HEALTH'],
    'tomcat_levels': ['WARN','ERROR','FATAL','SEVERE']
}
