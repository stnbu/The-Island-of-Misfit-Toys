#!/Users/miburr/virtualenv/bin/python

import re
import os
import sys
from dulwich.repo import Repo
import logging
import pyhooklib

pyhooklib.log_comprehensive_call_details()

enum = object

DEFAULT_REFCHANGE_TYPE = enum()
CREATE_BRANCH = enum()
DELETE_BRANCH = enum()
CREATE_TRACKING_BRANCH = enum()
DELETE_TRACKING_BRANCH = enum()
CREATE_UNANNOTATED_TAG = enum()
DELETE_TAG = enum()
MODIFY_TAG = enum()

logger = logging.getLogger(__name__)
log_level = logging.DEBUG
logger.setLevel(log_level)
console = logging.StreamHandler()
console.setLevel(log_level)
logger.addHandler(console)

ZERO_REV = '0'*40

class Perms(object):
    conf_option_names = [
        'branchre',
    ]

    def __init__(self, repo=None):
        self.repo = repo
        if self.repo is not None:
            self.get()

    def get(self, repo=None):
        logger.debug('Getting perms info.')
        if repo is not None:
            _repo = repo
        else:
            _repo = self.repo
        config = _repo.get_config()
        for name in self.conf_option_names:
            value = config.get('hooks', name)
            self.__dict__[name] = value

class Ref(str):

    sep = '/'

    def __new__(cls, s):
        assert s.startswith('refs/'), 'does not start with "refs/" is that possible?'
        obj = str.__new__(cls, s)
        obj._type = None
        obj._shortname = None
        return obj

    @property
    def shortname(self):
        if self._shortname is None:
            _, _, shortname = self.split(self.sep, 2)
            self._shortname = shortname
        return self._shortname

    @property
    def type(self):
        if self._type is None:
            _, type, _ = self.split(self.sep, 2)
            # TODO validate
            self._type = type
        return self._type

class Rev(str):

    def __init__(self, s):
        str.__init__(self, s)
        self._type = None

    @property
    def type(self):
        if self._type is None:
            if str(self) == ZERO_REV:
                self._type = 'delete'
            else:
                logger.debug('system call to get to determine revtype of {0}'.format(repr(self)))
                self._type = pyhooklib.get_proc_output('git cat-file -t {0}'.format(self))
            self._type = self._type.strip()
        return self._type

class RefChange(object):

    def __init__(self, change):
        try:
            change = change.split()
        except AttributeError:
            pass

        refname, oldrev, newrev = change
        self.ref = Ref(refname)
        self.oldrev = Rev(oldrev)
        self.newrev = Rev(newrev)

        logger.debug('creating Repo() instance')
        self.repo = Repo(os.environ['GIT_DIR'])
        self.perms = Perms(self.repo)

    @property
    def type(self):
        type = None
        logger.debug('determining "type" of this ref change. (that is, what kind of change is actually being attempted?)')
        unhandled_case_message = 'While trying to determine ref change type, your particular case was not encountered!'
        if self.ref.type == 'heads':
            if self.newrev.type == 'commit':
                if self.oldrev == ZERO_REV:
                    type = CREATE_BRANCH
                else:
                    type = DEFAULT_REFCHANGE_TYPE
            elif self.newrev.type == 'delete':
                type = DELETE_BRANCH
            else:
                raise Exception(unhandled_case_message)
        elif self.ref.type == 'remotes':
            if self.newrev.type == 'commit':
                type = CREATE_TRACKING_BRANCH
            elif self.newrev.type == 'delete':
                type = DELETE_TRACKING_BRANCH
            else:
                raise Exception(unhandled_case_message)
        elif self.ref.type == 'tags':
            if self.newrev.type == 'commit':
                type = CREATE_UNANNOTATED_TAG
            elif self.newrev.type == 'delete':
                type = DELETE_TAG
            elif self.newrev.type == 'tag':
                try:
                    pyhooklib.get_proc_output('git rev-parse {0}'.format(self.ref))
                    parsable = True
                except:
                    parsable = False
                if parsable:
                    type = MODIFY_TAG
                else:
                    raise Exception(unhandled_case_message)
            else:
                raise Exception(unhandled_case_message)
        else:
            raise Exception(unhandled_case_message)

        if type is None:
            raise Exception('programming logic error: type was never set.')

        type_name, = [n for n,v in globals().iteritems() if v is type]
        logger.debug('determined that type is: {0}'.format(type_name))
        return type

    @property
    def permited(self):
        if self.type is DEFAULT_REFCHANGE_TYPE:
            return True
        elif self.type is CREATE_BRANCH:
            # examine branch name
            return re.match(self.perms.branchre, self.ref.shortname)
        else:
            pass  # boo
        return False

if __name__ == '__main__':
    if True:
        ref_change = RefChange(sys.argv[1:])
        if ref_change.permited:
            sys.exit(0)
        sys.exit(1)


    if False:
        d = '/Users/miburr/repoplay/repos/foo5.git'
        os.environ['GIT_DIR'] = d
        os.chdir(d)
        change = 'refs/heads/boo 0000000000000000000000000000000000000000 571a01c0ebc4a85caaae592ad51ecedf87b8fe28'
        change = 'refs/heads/master 0000000000000000000000000000000000000000 6908378c97b6ceaa2de4cd275cdb0bbc78ad3b5c'
        c=RefChange(change)
        c.ref.type
        c.ref.shortname
        c.oldrev.type
        c.newrev.type
        c.permited
        c.type
