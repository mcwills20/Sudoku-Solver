import pandas as pd
import solve_utils as utils
import cell


class Sudoku(object):

    def __init__(self, raw):

        self.sudoku = self.build_puzzle(raw)

    def build_puzzle(self, raw):
        # cast the raw data (which should be a string of numbers with no delimination) into a list for easier sorting
        lis = list(raw)
        # initialize a temporary formatted list. 9 Lists (the rows) of 9 numbers each will be put into this list
        formattedlis = []
        for i in range(0, 81, 9):
            formattedlis.append(lis[i:i+9])

        # covert the lists from the raw values into the Cell object types
        for rownum, row in enumerate(formattedlis):
            for colnum, val in enumerate(row):
                formattedlis[rownum][colnum] = cell.Cell(
                    int(val), rownum, colnum)

        # use the final list to return a pandas dataframe with the Cell objects
        return(pd.DataFrame(formattedlis))

    def basic_check(self, change):
        # Basic checks compare the value of other cells in the region. They remove all values found from the possible
        # values of cells in the region.

        for i in range(9):
            change, errorcode = self.bas_check_row(i, change)
            # Once one cell is solved, break out of the loop so the GUI updates
            if change:
                return change, errorcode
        for i in range(9):
            change, errorcode = self.bas_check_column(i, change)
            if change:
                return change, errorcode
        for i in range(9):
            change, errorcode = self.bas_check_box(i, change)
            if change:
                return change, errorcode

        return change, errorcode

    def bas_check_row(self, rownum, change):

        # Check which values exist in the row
        found = utils.check_values(self.sudoku.loc[rownum])

        # Assign possible values based on found, return if a cell has been solved or if there is an error
        return self.bas_assign_region(self.sudoku.loc[rownum], change, found)

    def bas_check_column(self, colnum, change):

        # Check which values exist in the column
        found = utils.check_values(self.sudoku.loc[:, colnum])

        # Assign possible values based on found, return if a cell has been solved or if there is an error
        return self.bas_assign_region(self.sudoku.loc[:, colnum], change, found)

    def bas_check_box(self, boxnum, change):

        # Slice the board into the correct box
        box = utils.get_box(boxnum, self.sudoku)

        # Check which values exist in the box
        found = utils.check_values_box(box)

        # Assign possible values based on found, return if a cell has been solved or if there is an error
        return self.bas_assign_region(utils.iter_box(box), change, found)

    def bas_assign_region(self, region, change, found):

        errorcode = 0

        # Assign the possible values. Found values cannot be possible
        for cell in region:
            if not cell.solved:
                change, errorcode = cell.assign_possible(
                    found, change, self.sudoku)
                if change:
                    return change, errorcode

        return change, errorcode

    def intermediate_check(self, change):
        # Intermediate checks will check the possible values of the cells in a region
        # If only one cell in a region has a specfic possible value, that can be considered solved

        for i in range(9):
            change, errorcode = self.int_check_row(i, change)
            if change:
                return change, errorcode
        for i in range(9):
            change, errorcode = self.int_check_column(i, change)
            if change:
                return change, errorcode
        for i in range(9):
            change, errorcode = self.int_check_box(i, change)
            if change:
                return change, errorcode

        return change, errorcode

    def int_check_row(self, rownum, change):

        found = utils.check_values(self.sudoku.loc[rownum])
        errorcode = 0

        return self.int_check_region(self.sudoku.loc[rownum], found, errorcode, change)

    def int_check_column(self, colnum, change):

        found = utils.check_values(self.sudoku.loc[:, colnum])
        errorcode = 0

        return self.int_check_region(self.sudoku.loc[:, colnum], found, errorcode,  change)

    def int_check_region(self, region, found, errorcode, change):

        for cell in region:
            if not cell.solved:
                # Create a temporary list of possible values to check for
                possible = cell.possible.copy()
                # Remove any found values from temporary list
                for val in found:
                    if val in possible:
                        possible.remove(val)

                # Loop through the other cells in the row to find their possible values
                for checkcell in region:
                    # Only check if the cell isn't solved and it isn't the cell we are comparing to
                    if not checkcell.solved and cell != checkcell:
                        # Loop through all the possible values in the check cell
                        for pos in checkcell.possible:
                            # If a value is in the source, remove it
                            if pos in possible:
                                possible.remove(pos)

                # If there is only one possible solution left, that must be the solution for this cell.
                if len(possible) == 1:
                    cell.possible = possible.copy()
                    change, errorcode = cell.check_solved(change, self.sudoku)
                    if change:
                        return change, errorcode

        return change, errorcode

    def int_check_box(self, boxnum, change):

        # Slice the board into the correct box
        box = utils.get_box(boxnum, self.sudoku)

        found = utils.check_values_box(box)
        errorcode = 0

        # Start checking the cells in the box. Cannot use int_check_region due needing to use the iter_box generator
        for cell in utils.iter_box(box):
            if not cell.solved:
                # Create a tempoarty list of possible values to check for
                possible = cell.possible.difference(found)

                # Loop through the other cells in the quardrant to find their possible values
                for checkcell in utils.iter_box(box):
                    # Only check if the cell isn't solved and it isn't the cell we are comparing to
                    if not checkcell.solved and cell != checkcell:
                        for pos in checkcell.possible:
                            # If there is a value that is in the source possible list, remove it
                            if pos in possible:
                                possible.remove(pos)

                # If there is only one possible solution left, that must be the solution for this cell
                if len(possible) == 1:
                    cell.possible = possible.copy()
                    change, errorcode = cell.check_solved(change, self.sudoku)
                    if change:
                        return change, errorcode

        return change, errorcode

    def cross_check(self, change):
        # Cross checks will compare the solution state of rows, columns, and boxes to remove possible values
        for i in range(9):
            change, errorcode = self.box_to_row_check(i, change)
            if change:
                return change, errorcode
        for i in range(9):
            change, errorcode = self.box_to_col_check(i, change)
            if change:
                return change, errorcode
        for i in range(9):
            change, errorcode = self.row_to_box_check(i,  change)
            if change:
                return change, errorcode
        for i in range(9):
            change, errorcode = self.col_to_box_check(i, change)
            if change:
                return change, errorcode

        return change, errorcode

    def box_to_row_check(self, boxnum, change):
        # Determines if two rows are solved in a particular box, the unsolved row must contain the missing values
        # Thus, you can remove these missing values from the cells located in this row in other boxes

        box = utils.get_box(boxnum, self.sudoku)
        errorcode = 0
        # Check to see if two rows are completed within the box
        incomplete_rows = set()

        for i, local_row in enumerate(box.itertuples(index=False)):
            row_complete = True
            for cell in local_row:
                if cell.value == 0:
                    row_complete = False

            if not row_complete:
                incomplete_rows.add(i)

        if len(incomplete_rows) == 1:

            row = self.sudoku.loc[utils.eval_row(
                boxnum, incomplete_rows.pop())]

            return self.remove_from_other_boxes(row, box, boxnum, change)

        else:
            return change, errorcode

    def box_to_col_check(self, boxnum, change):
        # Determines if two columns are solved in a particular box, the unsolved columns must contain the missing values
        # Thus, you can remove these missing values from the cells located in this columns in other boxes

        box = utils.get_box(boxnum, self.sudoku)
        errorcode = 0
        incomplete_cols = set()

        for i, local_col in box.iteritems():
            col_complete = True
            for cell in local_col.values:
                if cell.value == 0:
                    col_complete = False

            if not col_complete:
                incomplete_cols.add(i)

        if len(incomplete_cols) == 1:

            column = self.sudoku.loc[:, incomplete_cols.pop()]

            return self.remove_from_other_boxes(column, box, boxnum, change)

        else:
            return change, errorcode

    def remove_from_other_boxes(self, region, box, boxnum, change):

        errorcode = 0

        found = utils.check_values_box(box)
        remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)

        for cell in region:
            if not cell.solved and cell.box != boxnum:
                change, errorcode = cell.assign_possible(
                    remove_pos, change, self.sudoku)

        return change, errorcode

    def row_to_box_check(self, rownum, change):
        # Determines, within a row, if 2 boxes have been completed. If they have, the outstanding values in that row must be placed in the remaining
        # cells in the row. Thus it is not possible to place them in any other location in that box, so remove them from the possible values of other cells in that box

        found = utils.check_values(self.sudoku.loc[rownum])
        errorcode = 0
        # Only check if 6 or more values have been filled in, as any less means 2 boxes couldn't have been solved
        if len(found) > 5:

            incompleted_boxes = utils.eval_boxes(self.sudoku.loc[rownum])

            if len(incompleted_boxes) == 1:

                remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)
                box = utils.get_box(incompleted_boxes.pop(), self.sudoku)

                for cell in utils.iter_box(box):
                    if not cell.solved and cell.row != rownum:
                        change, errorcode = cell.assign_possible(
                            remove_pos, change, self.sudoku)

        return change, errorcode

    def col_to_box_check(self, colnum, change):
        # Determines, within a column, if 2 boxes have been completed. If they have, the outstanding values in that column must be placed in the remaining
        # cells in the column. Thus it is not possible to place them in any other location in that box, so remove them from the possible values of other cells in that box

        found = utils.check_values(self.sudoku.loc[:, colnum])
        errorcode = 0
        if len(found) > 5:

            incompleted_boxes = utils.eval_boxes(self.sudoku.loc[:, colnum])

            if len(incompleted_boxes) == 1:

                remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)
                box = utils.get_box(incompleted_boxes.pop(), self.sudoku)

                for cell in utils.iter_box(box):
                    if not cell.solved and cell.column != colnum:
                        change, errorcode = cell.assign_possible(
                            remove_pos, change, self.sudoku)

        return change, errorcode

    def compare_answer(self, solution):
        # Function to compare the answer to the solved puzzle. Current not in use
        solved = True

        for rownum in range(9):
            for colnum in range(9):
                if self.sudoku.loc[rownum, colnum].value != solution.loc[rownum, colnum].value:
                    solved = False

        return solved

    def validate_answer(self, final=False):
        # Function to validate the answer if the solution is not known

        solved = True

        solved, error = self.validate_rows(solved)

        solved, error = self.validate_columns(solved)

        solved, error = self.validate_boxes(solved)

        return solved, error

    def validate_rows(self, solved):

        for rownum in range(9):
            solved, error = self.validate_region(
                self.sudoku.loc[rownum], solved)

            if error:
                return solved, error

        return solved, error

    def validate_columns(self, solved):

        for colnum in range(9):
            solved, error = self.validate_region(
                self.sudoku.loc[:, colnum], solved)

            if error:
                return solved, error

        return solved, error

    def validate_boxes(self, solved):

        for boxnum in range(9):
            box = utils.get_box(boxnum, self.sudoku)
            solved, error = self.validate_box(box, solved)

            if error:
                return solved, error

        return solved, error

    def validate_region(self, region, solved):

        found = set()
        error = False
        for cell in region:
            if cell.value in found:
                error = True
                utils.color_red(region)
            elif cell.value != 0:
                found.add(cell.value)

        # Solved by default is true during the validate_answer call. If all 9 values are not found, then it is not solved
        if len(found) != 9:
            solved = False

        return solved, error

    def validate_box(self, box, solved):

        found = set()
        error = False
        for cell in utils.iter_box(box):
            if cell.value in found:
                error = True
                utils.color_red_box(box)
            elif cell.value != 0:
                found.add(cell.value)

        # Solved by default is true during the validate_answer call. If all 9 values are not found, then it is not solved
        if len(found) != 9:
            solved = False

        return solved, error
