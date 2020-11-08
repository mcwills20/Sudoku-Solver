import pandas as pd


class Box(object):

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column

        # Get what quadrant the block is in. Useful for checking later
        self.quad = self.get_quad()
        # Initialize the possible dict
        self.init_possible()

    # When printing, display the value
    def __repr__(self):
        return str(self.value)

    def get_quad(self):

        if self.row <= 2:
            # Upper left
            if self.column <= 2:
                return 0
            # Upper Right
            elif self.column >= 6:
                return 2
            # Upper Middle
            else:
                return 1
        elif self.row >= 6:
            # Middle Left
            if self.column <= 2:
                return 3
            # Middle Right
            elif self.column >= 6:
                return 5
            # True Middle
            else:
                return 4
        else:
            # Lower Left
            if self.column <= 2:
                return 6
            # Lower Right
            elif self.column >= 6:
                return 8
            # Lower Middle
            else:
                return 7

    def init_possible(self):
        if self.value == 0:
            self.solved = False
            self.possible = [i for i in range(1, 10)]
        else:
            self.solved = True
            self.possible = [self.value]

    def assign_possible(self, found):
        for val in found:
            if val in self.possible:
                self.possible.remove(val)

        self.check_solved()

    def check_solved(self):

        if len(self.possible) == 1:
            self.solved = True
            self.value = self.possible[0]
            print(str(self.row) + ','+str(self.column) +
                  ' has been solved as '+str(self.value))


def build_sudoku(raw):
    # cast the raw data (which should be a string of numbers with no delimination) into a list for easier sorting
    _lis = list(raw)
    # initialize a temporary formatted list. 9 Lists (the rows) of 9 numbers each will be put into this list
    _formattedlis = []
    for i in range(0, 81, 9):
        _formattedlis.append(_lis[i:i+9])

    # covert the lists from the raw values into the box object types
    for rownum, row in enumerate(_formattedlis):
        for colnum, val in enumerate(row):
            _formattedlis[rownum][colnum] = Box(int(val), rownum, colnum)

    # use the final list to return a pandas dataframe with the box objects
    return pd.DataFrame(_formattedlis)
