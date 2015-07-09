
import copy
import sys
import select

import os
import logging
import subprocess

logger = logging.getLogger(__name__)
log_level = logging.DEBUG
logger.setLevel(log_level)
console = logging.StreamHandler()
console.setLevel(log_level)
logger.addHandler(console)

logger.debug('crazy-helpful logging enabled...')

def get_proc_output(cmd):
    try:
        cmd = cmd.split()
    except AttributeError:
        pass
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    retcode = process.poll()
    if retcode:
        raise Exception('Process said:\n{0} (Exit Val {1})'.format(err, retcode))
    return output

def log_comprehensive_call_details(logger_=None):
    if logger_ is None:
        logger_ = logger
    r, _, _ = select.select([sys.stdin], [], [], 0)
    stdin = None
    if r:
        stdin = sys.stdin.read()
    environ = copy.copy(os.environ)
    argv = sys.argv
    stdin = str(stdin)
    for line in stdin.splitlines():
        logger_.debug('stdin: '+line)
    for key, value in environ.iteritems():
        logger_.debug('environ: {0}: {1}'.format(key, value))
    for index, value in enumerate(argv):
        logger_.debug('argv: {0}: {1}'.format(index, value))

