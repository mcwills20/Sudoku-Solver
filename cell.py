import pandas as pd
import solve_utils as utils


class Cell(object):

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column

        # Find the index of the GUI interface
        self.gui = None
        # Get what box the cell is in. Useful for checking later
        self.box = self.init_box()
        # Initialize the possible list
        self.init_possible()

        # Assign values for backtracking
        self.assign_next()
        self.assign_previous()
        self.mutable = self.value == 0
        self.new = True

    # When printing, display the value
    def __repr__(self):
        return str(self.value)

    def init_box(self):

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
        elif self.row <= 5:
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
            self.original = False
            self.possible = set([i for i in range(1, 10)])
        else:
            self.solved = True
            self.original = True
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
        # Set mutable to false so it will not be overwritten during backtracking
        self.mutable = False

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
        _, errorrow = utils.validate_region(sudoku.loc[self.row], True)
        # Check Column
        _, errorcol = utils.validate_region(sudoku.loc[:, self.column], True)
        # Check box
        box = utils.get_box(self.box, sudoku)
        _, errorbox = utils.validate_box(box, True)

        return errorrow or errorcol or errorbox

    def reinit(self):
        self.solved = False
        self.value = 0
        self.gui.value = 0
        self.mutable = True
        self.original = False
        self.new = True
        self.tpossible = set()
        self.gui.ids.pos5.font_size = 15
        self.gui.ids.pos5.text = ''
        self.gui.ids.pos5.color = [0, 0, 0, .3]
        self.gui.color = [1, 1, 1, 1]
        self.init_possible()
        self.gui.initialize()

    def assign_next(self):

        if self.row == 8 and self.column == 8:
            self.next = ('End', 'End')

        elif self.column == 8:
            self.next = (self.row + 1, 0)

        else:
            self.next = (self.row, self.column + 1)

    def assign_previous(self):

        if self.row == 0 and self.column == 0:
            self.previous = ('Beginning', 'Beginning')

        elif self.column == 0:
            self.previous = (self.row - 1, 8)

        else:
            self.previous = (self.row, self.column - 1)
