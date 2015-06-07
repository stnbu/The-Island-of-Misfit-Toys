
s = [
    [
[None, None, None], [None, None, None], [None, None, None],
[None, None, None], [None, None, None], [None, None, None],
[None, None, None], [None, None, None], [None, None, None],
    ],
    [
[None, None, None], [None, None, None], [None, None, None],
[None, None, None], [None, None, None], [None, None, None],
[None, None, None], [None, None, None], [None, None, None],
    ],
[
[None, None, None], [None, None, None], [None, None, None],
[None, None, None], [None, None, None], [None, None, None],
[None, None, None], [None, None, None], [None, None, None],
],
]

class Illegal(Exception):
    ""

class Row(list):
    def __init__(self, values=None):
        list.__init__(self, (None,)*3)
        if values is not None:
            for index, value in enumerate(values):
                self[index] = value
    def __setitem__(self, index, value):
        if value is not None and value in self:
            raise Illegal()##
        list.__setitem__(self, index, value)

class Square(list):
    def __init__(self, rows=None):
        list.__init__(self, (Row(),)*3)
        if rows is not None:
            for index, row in enumerate(rows):
                self[index] = row
    def __setitem__(self, index, row):
        for i, r in enumerate(self):
            if i == index:
                continue
            for v in r:
                if v is not None and v in row:
                    raise Illegal()
        list.__setitem__(self, index, row)

class Board(list):
    def __init__(self, board=None):
        list.__init__(self, ((Square(),)*3,)*3)
        if board is not None:
            for x, row in enumerate(board):
                for y, square in enumerate(row):
                    self[x][y] = square

    def xx__setitem__(self, index, row):
        for i, r in enumerate(self):
            if i == index:
                continue
            for v in r:
                if v is not None and v in row:
                    raise Illegal()
        list.__setitem__(self, index, row)

Board()

r1=Row([1,3,9])
r2=Row([None, None,4])
r3=Row([None, 2,7])
Square([r1,r2,r3])
