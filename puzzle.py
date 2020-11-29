import pandas as pd
import solve_utils as utils
import solve


class Cell(object):

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column

        # Find the index of the GUI interface
        self.gui = None

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
        elif self.row <= 6:
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
            self.possible = set([i for i in range(1, 10)])
        else:
            self.solved = True
            self.possible = set([self.value])

    def assign_possible(self, found, change, sudoku):
        self.possible = self.possible.difference(found)

        # Update the gui
        self.gui.update_possible(self.possible)

        change, errorcode = self.check_solved(change, sudoku)

        return change, errorcode

    def check_solved(self, solvedchange, sudoku):

        if len(self.possible) == 1:
            self.assign_solution(self.possible.pop())
            solvedchange = True
            if self.check_double(sudoku):
                errorcode = 2
            else:
                errorcode = 0
        else:
            errorchange, errorcode = self.check_possible(sudoku)

        # If there is an error, the errorchange variable will be set to true, which will cause the solve function to return early
        change = solvedchange or errorchange

        return change, errorcode

    def assign_solution(self, solution):
        self.solved = True
        self.value = solution

        # Update the gui
        self.gui.update_solution(self.value)

    def check_possible(self, sudoku):

        if len(self.possible) == 0 and not self.solved:
            # Set the background color to red
            self.gui.color = [1, 0, 0, 1]
            # Returns errorchange True, which causes the solve function to return after this step
            return True, 1

        else:
            # Returns errorchange False, which lets the solve function continue as normal
            return False, 0

    def check_double(self, sudoku):

        # Check Row
        _, errorrow = solve.validate_region(sudoku.loc[self.row], True)
        # Check Column
        _, errorcol = solve.validate_region(sudoku.loc[:, self.column], True)
        # Check quadrant
        quadrant = utils.get_quad(self.quad, sudoku)
        _, errorquad = solve.validate_quadrant(quadrant, True)

        return errorrow or errorcol or errorquad

    def reinit(self):
        self.solved = False
        self.value = 0
        self.gui.value = 0
        self.gui.ids.pos5.font_size = 15
        self.gui.ids.pos5.text = ''
        self.gui.ids.pos5.color = [0, 0, 0, .3]
        self.gui.color = [1, 1, 1, 1]
        self.init_possible()
        self.gui.initialize()


def build_sudoku(raw):
    # cast the raw data (which should be a string of numbers with no delimination) into a list for easier sorting
    lis = list(raw)
    # initialize a temporary formatted list. 9 Lists (the rows) of 9 numbers each will be put into this list
    formattedlis = []
    for i in range(0, 81, 9):
        formattedlis.append(lis[i:i+9])

    # covert the lists from the raw values into the Cell object types
    for rownum, row in enumerate(formattedlis):
        for colnum, val in enumerate(row):
            formattedlis[rownum][colnum] = Cell(int(val), rownum, colnum)

    # use the final list to return a pandas dataframe with the Cell objects
    return pd.DataFrame(formattedlis)
