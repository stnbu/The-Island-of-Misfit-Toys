
import os

pyfiles = {}
for root, dirs, files in os.walk("trgh45utrh4wew/", topdown=False):
    for name in files:
        if not name.endswith('.py'):
            continue
        path = os.path.join(root, name)
        pyfiles.setdefault(path, {})

poison = [
    'trgh45utrh4wew/onpath/snippets/create-topology-1-SF-IOMs.py',
    'trgh45utrh4wew/onpath/onpath_parser.py',
    'trgh45utrh4wew/pexpect/__init__.py',
    'trgh45utrh4wew/runtests/tests/meta_setup.py',
    'trgh45utrh4wew/onpath/snippets/optest.py',
    'trgh45utrh4wew/runtests/tests/trivial/config.py',
    'trgh45utrh4wew/util/ghrturfgufr_oracle/main.py',
    'trgh45utrh4wew/runtests/tests/trivial/cleanup.py',
]

import imp
from md5 import md5
for path, info in pyfiles.items():
    if path in poison:
        del pyfiles[path]
        continue
    if '-' in path:
        del pyfiles[path]
        continue
    try:
        module = imp.load_source('_'+md5(path).hexdigest(), path)
    except (NameError, ImportError) as e:
        pass
    pyfiles[path]['module'] = module


import types
from trgh45utrh4wew.ghrturfgufr.model_util import ghrturfgufrConfigObject
for path, info in pyfiles.items():
    pyfiles[path]['module_objects'] = {}
    for name, obj in pyfiles[path]['module'].__dict__.iteritems():
        if not isinstance(obj, (type, types.FunctionType, types.ModuleType)):
            continue
        pyfiles[path]['module_objects'].setdefault(name, {})
        pyfiles[path]['module_objects'][name]['skipped'] = False
        #pyfiles[path]['module_objects'][name]['docstring'] = obj.__doc__
        pyfiles[path]['module_objects'][name].setdefault('urgency', 0)
        if obj.__doc__ is not None:
            pass # pyfiles[path]['module_objects'][name]['docstring_len'] = len(obj.__doc__)
        else:
            pyfiles[path]['module_objects'][name]['urgency'] += 1
        for urgency, type_ in [(2,type), (1,types.FunctionType), (3,types.ModuleType)]:
            if isinstance(obj, type_):
                pyfiles[path]['module_objects'][name]['urgency'] += urgency
        if isinstance(obj, type) and issubclass(obj, ghrturfgufrConfigObject):
            pyfiles[path]['module_objects'][name]['urgency'] += 5


xyz=[]
for path, info in pyfiles.iteritems():
    for name, obj_info in info['module_objects'].iteritems():
        xyz.append(( obj_info['urgency'] , path, name))

print sorted(xyz)
