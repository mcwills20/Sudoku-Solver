import pandas as pd


class Box(object):

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column

        # Find the index of the GUI interface
        self.index = convert_index(self.row, self.column)

        # Get what quadrant the block is in. Useful for checking later
        self.quad = self.init_quad()
        # Initialize the possible list
        self.init_possible()

    # When printing, display the value
    def __repr__(self):
        return str(self.value)

    def init_quad(self):

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

    def assign_possible(self, gui, found, change):
        for val in found:
            if val in self.possible:
                self.possible.remove(val)

        # Update the gui
        gui.cell_list[self.index].update_possible(self.possible)

        change = self.check_solved(gui, change)
        return change

    def check_solved(self, gui, change):

        if len(self.possible) == 1:
            self.solved = True
            self.value = self.possible[0]
            change = True

            # Update the gui
            ind = convert_index(self.row, self.column)
            gui.cell_list[ind].update_solution(self.value)

        return change


def build_sudoku(raw):
    # cast the raw data (which should be a string of numbers with no delimination) into a list for easier sorting
    lis = list(raw)
    # initialize a temporary formatted list. 9 Lists (the rows) of 9 numbers each will be put into this list
    formattedlis = []
    for i in range(0, 81, 9):
        formattedlis.append(lis[i:i+9])

    # covert the lists from the raw values into the box object types
    for rownum, row in enumerate(formattedlis):
        for colnum, val in enumerate(row):
            formattedlis[rownum][colnum] = Box(int(val), rownum, colnum)

    # use the final list to return a pandas dataframe with the box objects
    return pd.DataFrame(formattedlis)


def convert_index(rownum, colnum):
    index = -((rownum * 9) + colnum + 1)
    return index
