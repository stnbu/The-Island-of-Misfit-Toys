



class Board(object):

    def __init__(self, board):
        self.data = []
        def blah():
            return [None]*9
        for y in xrange(9):
            self.data.append(blah())
        for x, y, value in self._iter(board):
            self.update(x, y, value)

    def update(self, x, y, value):
        if value is not None:
            if value in self.get_row(y):
                raise Exception('row')
            if value in self.get_column(x):
                raise Exception('col')
            if value in self.get_square(x,y):
                raise Exception('sq')
        self.data[y][x] = value

    def get_square(self, x, y):
        base_x = int(x/3) * 3
        base_y = int(y/3) * 3
        x_range = range(base_x,base_x+3)
        y_range = range(base_y,base_y+3)
        for x, y, value in self._iter(self.data):
            if x in x_range and y in y_range:
                yield value

    def get_row(self, y):
        return self.data[y]

    def get_column(self, x):
        for _x, _, value in self._iter(self.data):
            if _x!=x: continue
            yield(value)

    def _iter(self, data):
        for y, column in enumerate(data):
            for x, value in enumerate(column):
                yield x, y, value

    def __repr__(self):
        r=''
        for x, y, value in self._iter(self.data):
            r += '.' if value is None else str(value)
            if x in [2,5]:
                r+='|'
            if x==8:
                r+='\n'
                if y in [2,5]:
                    r+='_'*11+'\n'
        return r



if False:
    board = [[None]*9]*9
    b = Board(board)
    b.update(0,0,1)
    b.update(8,0,2)
    b.update(0,8,3)
    b.update(8,8,4)
    v=0
    for y in xrange(3,6):
        for x in xrange(3,6):
            b.update(x,y,v)
            v+=1
    #print b
    #print list(b.get_square(3,3))
    assert b.get_row(0) == [1, None, None, None, None, None, None, None, 2]
    assert list(b.get_column(0)) == [1, None, None, None, None, None, None, None, 3]
    print b
