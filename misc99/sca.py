
import shlex

class SmartElement(list):

    def __init__(self, string):
        self.string = string
        self.dent = len(self.string) - len(self.string.lstrip())
        lex = shlex.shlex(self.string, posix=True)
        lex.whitespace_split = True
        lex.commenters = ''
        list.__init__(self)
        for e in lex:
            self.append(e)

    def _classify(self):
        raise NotImplementedError('Implement your own "_classify".')

    @property
    def starts_block(self):
        raise NotImplementedError('Try implementing "_classify" and calling it here.')

    @property
    def ends_block(self):
        raise NotImplementedError('Try implementing "_classify" and calling it here.')

    def __str__(self):
        return self.string


class Block(object):

    element_type = SmartElement

    def __init__(self, parent=None, blocks=None):
        self.parent = parent
        if self.parent is not None and self not in self.parent.children:
            self.parent.append_child(self)
        self.children = []
        if blocks is not None:
            if self.parent is not None:
                raise TypeError('Can not yet handle values for both "blocks" and "parent"')
            self._recurse_new_blocks(blocks)

    def append_child(self, child):
        self.children.append(child)

    def _recurse_new_blocks(self, blocks):

        current_block = self

        new_block_type = self.__class__

        for line in blocks:
            line = self.element_type(line)
            if line.starts_block:
                current_block = new_block_type(parent=current_block)
                current_block.append_child(line)
            elif line.ends_block:
                current_block.append_child(line)
                current_block = current_block.parent
            else:
                current_block.append_child(line)

    def _get_lines(self):
        lines = []
        for child in self.children:
            if isinstance(child, self.element_type):
                lines.append(child)
            elif isinstance(child, self.__class__):
                l = child._get_lines()
                lines.extend(l)
            else:
                ValueError(child)
        return lines


    def __str__(self):
        lines = self._get_lines()
        lines = map(str, lines)
        return ''.join(lines)


    @property
    def dent(self):
        for child in self.children:
            return child.dent
        else:
            return 0

class MOInfo(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.iterkeys():
            setattr(self, name, value)

class ConfigLine(SmartElement):

    START = 0
    END = 1
    UNKNOWN = 2

    def __init__(self, string):
        SmartElement.__init__(self, string)
        self.mo_info = MOInfo()
        self.parent_block = None

    @property
    def verb(self):   # I can't bring myself to use explicit indicies
        for word in self:
            return word
        else:
            return None

    @property
    def context_keyword(self):
        return self[1]

    def find_class(self, context_keyword):
        return 'XXXX'

    def _classify(self):
        if self.verb in ['create', 'enter', 'scope']:
            self.mo_info.cls = self.find_class(self.context_keyword)
            return self.START
        elif self.verb in ['exit']:
            return self.END
        else:
            return self.UNKNOWN

    @property
    def starts_block(self):
        return self._classify() is self.START

    @property
    def ends_block(self):
        return self._classify() is self.END


class ConfigBlock(Block):

    element_type = ConfigLine

    def handle_new_child_side_effects(self, child):
        pass

    def append_child(self, child):
        child.parent_block = self
        self.handle_new_child_side_effects(child)
        Block.append_child(self, child)


if __name__ == '__main__':
    blocks = """\
    scope server 8
        scope diag
            set run-policy-name ""
        exit
    exit
    """
    from StringIO import StringIO
    blocks = StringIO(blocks)
    blocks = open('/tmp/sca.txt', 'r')
    r = ConfigBlock(blocks=blocks)
    print r
