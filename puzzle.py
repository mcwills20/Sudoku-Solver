import pandas as pd


class box(object):

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column

        # Get what quadrant the block is in. Useful for checking later
        self.quad = self.getquad()
        # Initialize the possible dict
        self.initpossible()

    # When printing, display the value    
    def __repr__(self):
        return str(self.value)


    def getquad(self):

        if self.row <= 2:
            # Upper left
            if self.column <= 2:
                return 1
            # Upper Right
            elif self.column >= 6:
                return 3
            # Upper Middle
            else:
                return 2
        elif self.row >= 6:
            # Middle Left
            if self.column <= 2:
                return 4
            # Middle Right
            elif self.column >= 6:
                return 6
            # True Middle
            else:
                return 5
        else:
            # Lower Left
            if self.column <= 2:
                return 7
            # Lower Right
            elif self.column >= 6:
                return 9
            # Lower Middle
            else:
                return 8


    def initpossible(self):
        self.possible = dict()
        if self.value == 0:
            for i in range(1,10):
                self.possible[i] = True
        else:
            for i in range(1,10):
                self.possible[i] = False

            self.possible[self.value] = True

def build_puzzle(raw):
    # cast the raw data (which should be a string of numbers with no delimination) into a list for easier sorting
    _lis = list(str(raw))
    # initialize a temporary formatted list. 9 Lists (the rows) of 9 numbers each will be put into this list
    _formattedlis = []
    for i in range(0,81,9):
        _formattedlis.append(_lis[i:i+9])

    # use the formatted puzzle to create a list of box objects
    _finallis = []
    for rownum, row in enumerate(_formattedlis):
        _row = []
        for colnum, val in enumerate(row):
            _row.append(box(int(val), rownum, colnum))
        _finallis.append(_row)
    
    # use the final list to return a pandas dataframe with the box objects

    return pd.DataFrame(_finallis)
