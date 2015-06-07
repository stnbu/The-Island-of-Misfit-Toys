
def coerce_keys(*args, **kwargs):
    """This is a decorator for sub-types of dict.

    Coerce dict keys (whether reading or writing) using the supplied function (int by default). Keys are stored
    after corecion.
    """

    # The default "coercer". So we'll have "x[1] is x['1']" etc.
    func = int

    def wrapper(cls):
        """Actually wrap the class with this function. A "decorator" (of sorts.)
        """

        # how we find which argument to manipulate and how to manipulate it.
        flavors = {
            'key': {'key': 0},
            'mapping': {'mapping': 0},
        }

        def dress_keys(name, flavor):
            # wraps method called "name" using the "flavor" to decide what to do with the args (above.)

            def meth(*args, **kwargs):
                inst = args[0]
                args = args[1:]
                argspec = flavors[flavor]
                newargs = []
                for index, arg in enumerate(args):
                    if 'key' in argspec and index == argspec['key']:
                        arg = func(arg)
                    if 'mapping' in argspec and index == argspec['mapping']:
                        try:
                            arg = [(func(k),v) for k,v in arg.iteritems()]
                        except AttributeError:
                            arg = [(func(k),v) for k,v in arg]
                        if kwargs:
                            arg.extend([(func(k),v) for k,v in kwargs.iteritems()])
                    newargs.append(arg)
                args = tuple(newargs)
                orig = getattr(dict, name)
                return orig(inst, *args)
            return meth

        # these have a "key" arg (and possibly other args.)
        for name in ['__setitem__', '__getitem__', '__contains__']:
            attr = dress_keys(name, flavor='key')
            setattr(cls, name, attr)

        # these have mapping-like args: x({1:2}, foo=7)
        for name in ['__init__', 'update']:
            attr = dress_keys(name, flavor='mapping')
            setattr(cls, name, attr)
        return cls

    if not kwargs:
        # @deco()
        if not args:
            return wrapper
        # @deco
        elif issubclass(args[0], (dict,)):
            return wrapper(*args)
        # @deco(fun)
        else:
            func, = args
            return wrapper
    else:
        # @deco(kwarg=foo)
        func = kwargs['func']
        return wrapper

@coerce_keys
class NumericallyIndexedDict(dict):
    """A dictionary whose keys are "int", BUT will accept strings such that "num==int('string')". Also:

    >>> d = NumericallyIndexedDict()
    >>> d['1'] = object()
    >>> d['1'] is d[1]
    True
    >>> d[2] = object()
    >>> d['2'] is d[2]
    True
    >>>

    ...etc
    """

class DotSyntaxHierarchy(object):
    """This class' only purpose is to be "syntax sugar" and allow for the existence of "something" in
    "obj1.something.obj2", where no other logical type for "something" exists.

    TODO: Perhaps make sure this class is not abused and used for anything other than what's described above.
    """

import inspect
import tokenize
class DocstringManipulator(object):

    def __init__(self, obj, docstring=None):
        self.obj = obj
        self.docstring = self.get_current_docstring()
        self.docstring_coordinates = self.get_docstring_coordinates()

    @property
    def filename(self):
        return inspect.getsourcefile(self.obj)

    @property
    def source_file_object(self):
        return open(self.filename, 'r')

    def get_current_docstring(self):
        return inspect.getdoc(self.obj)

    @property
    def lineno(self):
        _, lineno = inspect.findsource(self.obj)
        return lineno

    def get_docstring_coordinates(self):
        f = self.source_file_object
        readline = f.readline
        for _ in xrange(self.lineno):
            readline()
        g = tokenize.generate_tokens(readline)   # tokenize the string
        for token_type, _, begin, end, _  in g:
            if token_type == tokenize.STRING:
                b = begin[0]+self.lineno, begin[1]
                e = end[0]+self.lineno, end[1]
                return b, e

    def get_split_lines(self):
        before_lines = []
        after_lines = []
        doc_lines = []
        begin, end = self.get_docstring_coordinates()
        f = self.source_file_object
        for _ in xrange(begin[0]-1):
            before_lines.append(f.readline())

        col_span = end[0] - begin[0]
        for _ in xrange(col_span+1):
            doc_lines.append(f.readline())

        while True:
            l = f.readline()
            if l == '':  # this indicates EOF. Trailing '\n' are preserved.
                break
            after_lines.append(l)

        return before_lines, doc_lines, after_lines

    @property
    def object_type(self):
        for t in [types.ModuleType, types.FunctionType, types.ClassType, types.MethodType, type]:
            if isinstance(self.obj, t):
                return t
        else:
            raise ValueError('Do not know how to edit docstring for type {0} (obj was {1})'.format(repr(t), repr(self)))

