__author__ = 'charls'

INTERNAL_MW_INT = 'internal-errors-mw-int'
INTERNAL_MW = 'errors-mw-int'
SNDRCVMSG = 'sndrcvmsgs'


dictionary = {
    INTERNAL_MW_INT: ['Integrator-Internal-SocieChat',
                               'PT-Internal-Middleware'],
    INTERNAL_MW: ['Integrator-Error-SocieChat',
                      'PT-Error-Middleware'],
    SNDRCVMSG: ['Integrator-SndRcvMsg-SocieChat','PT-SndRcvMsg-Middleware']
}

folders = {
    'middleware_folder': 'mw',
    'middleware_backups_folder': 'mwbkup'
}

logs = {
    'log_level': ['INTERNAL', 'STRUCTURE', 'LOSTMSG', 'ERROR', 'WARN', 'FUNCTIONAL', 'SNDRCVMSG', 'INFO', 'DEBUG',
                  'HEALTH']
}

