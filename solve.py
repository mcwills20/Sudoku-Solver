import solve_utils as utils

from copy import deepcopy


def basic_check(sudoku, change):
    # Basic checks compare the value of other cells in the region. They remove all values found from the possible
    # values of cells in the region.

    for i in range(9):
        change, errorcode = bas_check_row(i, sudoku, change)
        # Once one cell is solved, break out of the loop so the GUI updates
        if change:
            return change, errorcode
    for i in range(9):
        change, errorcode = bas_check_column(i, sudoku, change)
        if change:
            return change, errorcode
    for i in range(9):
        change, errorcode = bas_check_box(i, sudoku, change)
        if change:
            return change, errorcode

    return change, errorcode


def bas_check_row(rownum, sudoku, change):

    # Check which values exist in the row
    found = utils.check_values(sudoku.loc[rownum])

    # Assign possible values based on found, return if a cell has been solved or if there is an error
    return bas_check_region(sudoku.loc[rownum], sudoku, change, found)


def bas_check_column(colnum, sudoku, change):

    # Check which values exist in the column
    found = utils.check_values(sudoku.loc[:, colnum])

    # Assign possible values based on found, return if a cell has been solved or if there is an error
    return bas_check_region(sudoku.loc[:, colnum], sudoku, change, found)


def bas_check_box(boxnum, sudoku, change):

    # Slice the board into the correct box
    box = utils.get_box(boxnum, sudoku)

    # Check which values exist in the box
    found = utils.check_values_box(box)

    # Assign possible values based on found, return if a cell has been solved or if there is an error
    return bas_check_region(utils.iter_box(box), sudoku, change, found)


def bas_check_region(region, sudoku, change, found):

    errorcode = 0

    # Assign the possible values. Found values cannot be possible
    for cell in region:
        if not cell.solved:
            change, errorcode = cell.assign_possible(found, change, sudoku)
            if change:
                return change, errorcode

    return change, errorcode


def intermediate_check(sudoku, change):
    # Intermediate checks will check the possible values of the cells in a region
    # If only one cell in a region has a specfic possible value, that can be considered solved

    for i in range(9):
        change, errorcode = int_check_row(i, sudoku, change)
        if change:
            return change, errorcode
    for i in range(9):
        change, errorcode = int_check_column(i, sudoku, change)
        if change:
            return change, errorcode
    for i in range(9):
        change, errorcode = int_check_box(i, sudoku, change)
        if change:
            return change, errorcode

    return change, errorcode


def int_check_row(rownum, sudoku, change):

    found = utils.check_values(sudoku.loc[rownum])
    errorcode = 0

    return int_check_region(sudoku.loc[rownum], found, errorcode, sudoku, change)


def int_check_column(colnum, sudoku, change):

    found = utils.check_values(sudoku.loc[:, colnum])
    errorcode = 0

    return int_check_region(sudoku.loc[:, colnum], found, errorcode, sudoku, change)


def int_check_region(region, found, errorcode, sudoku, change):

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
                change, errorcode = cell.check_solved(change, sudoku)
                if change:
                    return change, errorcode

    return change, errorcode


def int_check_box(boxnum, sudoku, change):

    # Slice the board into the correct box
    box = utils.get_box(boxnum, sudoku)

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
                change, errorcode = cell.check_solved(change, sudoku)
                if change:
                    return change, errorcode

    return change, errorcode


def cross_check(sudoku, change):
    # Cross checks will compare the solution state of rows, columns, and boxes to remove possible values
    for i in range(9):
        change, errorcode = box_to_row_check(i, sudoku, change)
        if change:
            return change, errorcode
    for i in range(9):
        change, errorcode = box_to_col_check(i, sudoku, change)
        if change:
            return change, errorcode
    for i in range(9):
        change, errorcode = row_to_box_check(i, sudoku, change)
        if change:
            return change, errorcode
    for i in range(9):
        change, errorcode = col_to_box_check(i, sudoku, change)
        if change:
            return change, errorcode

    return change, errorcode


def box_to_row_check(boxnum, sudoku, change):
    # Determines if two rows are solved in a particular box, the unsolved row must contain the missing values
    # Thus, you can remove these missing values from the cells located in this row in other boxes

    box = utils.get_box(boxnum, sudoku)
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
        # Check which values to remove
        found = utils.check_values_box(box)
        remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)

        row = utils.eval_row(boxnum, incomplete_rows.pop())

        for cell in sudoku.loc[row]:
            if not cell.solved and cell.box != boxnum:
                change, errorcode = cell.assign_possible(
                    remove_pos, change, sudoku)

    return change, errorcode


def box_to_col_check(boxnum, sudoku, change):
    # Determines if two columns are solved in a particular box, the unsolved columns must contain the missing values
    # Thus, you can remove these missing values from the cells located in this columns in other boxes

    box = utils.get_box(boxnum, sudoku)
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
        found = utils.check_values_box(box)
        remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)

        column = incomplete_cols.pop()

        for cell in sudoku.loc[:, column]:
            if not cell.solved and cell.box != boxnum:
                change, errorcode = cell.assign_possible(
                    remove_pos, change, sudoku)

    return change, errorcode


def row_to_box_check(rownum, sudoku, change):
    # Determines, within a row, if 2 boxes have been completed. If they have, the outstanding values in that row must be placed in the remaining
    # cells in the row. Thus it is not possible to place them in any other location in that box.

    found = utils.check_values(sudoku.loc[rownum])
    errorcode = 0
    # Only check if 6 or more values have been filled in, as any less means 2 boxes couldn't have been solved
    if len(found) > 5:

        incompleted_boxes = utils.eval_boxes(sudoku.loc[rownum])

        if len(incompleted_boxes) == 1:

            remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)
            box = utils.get_box(incompleted_boxes.pop(), sudoku)

            for cell in utils.iter_box(box):
                if not cell.solved and cell.row != rownum:
                    change, errorcode = cell.assign_possible(
                        remove_pos, change, sudoku)

    return change, errorcode


def col_to_box_check(colnum, sudoku, change):
    # Determines, within a column, if 2 boxes have been completed. If they have, the outstanding values in that column must be placed in the remaining
    # cells in the column. Thus it is not possible to place them in any other location in that box.

    found = utils.check_values(sudoku.loc[:, colnum])
    errorcode = 0
    if len(found) > 5:

        incompleted_boxes = utils.eval_boxes(sudoku.loc[:, colnum])

        if len(incompleted_boxes) == 1:

            remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)
            box = utils.get_box(incompleted_boxes.pop(), sudoku)

            for cell in utils.iter_box(box):
                if not cell.solved and cell.column != colnum:
                    change, errorcode = cell.assign_possible(
                        remove_pos, change, sudoku)

    return change, errorcode


def compare_answer(sudoku, solution):
    # Function to compare the answer to the solved puzzle
    solved = True

    for rownum in range(9):
        for colnum in range(9):
            if sudoku.loc[rownum, colnum].value != solution.loc[rownum, colnum].value:
                solved = False

    return solved


def validate_answer(sudoku, final=False):
    # Function to validate the answer if the solution is not known

    solved = True

    solved, error = validate_rows(sudoku, solved)

    solved, error = validate_columns(sudoku, solved)

    solved, error = validate_boxes(sudoku, solved)

    return solved, error


def validate_rows(sudoku, solved):

    for rownum in range(9):
        solved, error = validate_region(sudoku.loc[rownum], solved)

        if error:
            return solved, error

    return solved, error


def validate_columns(sudoku, solved):

    for colnum in range(9):
        solved, error = validate_region(sudoku.loc[:, colnum], solved)

        if error:
            return solved, error

    return solved, error


def validate_boxes(sudoku, solved):

    for boxnum in range(9):
        box = utils.get_box(boxnum, sudoku)
        solved, error = validate_box(box, solved)

        if error:
            return solved, error

    return solved, error


def validate_region(region, solved):

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


def validate_box(box, solved):

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
