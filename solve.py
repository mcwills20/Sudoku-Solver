import solve_utils as utils


def basic_check(sudoku, change):
    # Basic checks compare the value of other cells in the region. They remove all values found from the possible
    # values of cells in the region.

    for i in range(9):
        change = bas_check_row(i, sudoku, change)
        # Once one cell is solved, break out of the loop so the GUI updates
        if change:
            return change
    for i in range(9):
        change = bas_check_column(i, sudoku, change)
        if change:
            return change
    for i in range(9):
        change = bas_check_quad(i, sudoku, change)
        if change:
            return change

    return change


def bas_check_row(rownum, sudoku, change):

    # Check which values exist in the row
    found = utils.check_values(sudoku.loc[rownum])

    # Assign the possible values. Found values cannot be possible
    for cell in sudoku.loc[rownum]:
        if not cell.solved:
            change = cell.assign_possible(found, change)
            if change:
                return change

    return change


def bas_check_column(colnum, sudoku, change):

    # Check which values exist in the column
    found = utils.check_values(sudoku.loc[:, colnum])

    # Assign the possible values. Found values cannot be possible
    for cell in sudoku.loc[:, colnum]:
        if not cell.solved:
            change = cell.assign_possible(found, change)
            if change:
                return change

    return change


def bas_check_quad(quad, sudoku, change):
    # Slice the board into the correct quadrant
    quadrant = utils.get_quad(quad, sudoku)

    # Check which values exist in the quadrant
    found = utils.check_values_quad(quadrant)

    # Assign the possible values. Found values cannot be possible
    for row in quadrant.itertuples(index=False):
        for cell in row:
            if not cell.solved:
                change = cell.assign_possible(found, change)
                if change:
                    return change

    return change


def intermediate_check(sudoku, change):
    # Intermediate checks will check the possible values of the cells in a region
    # If only one cell in a region has a specfic possible value, that can be considered solved

    for i in range(9):
        change = int_check_row(i, sudoku, change)
        if change:
            return change
    for i in range(9):
        change = int_check_column(i, sudoku, change)
        if change:
            return change
    for i in range(9):
        change = int_check_quad(i, sudoku, change)
        if change:
            return change

    return change


def int_check_row(rownum, sudoku, change):

    found = utils.check_values(sudoku.loc[rownum])

    for cell in sudoku.loc[rownum]:
        if not cell.solved:
            # Create a temporary list of possible values to check for
            possible = cell.possible.copy()
            # Remove any found values from temporary list
            for val in found:
                if val in possible:
                    possible.remove(val)

            # Loop through the other cells in the row to find their possible values
            for checkcell in sudoku.loc[rownum]:
                # Only check if the cell isn't solved and it isn't the cell we are comparing to
                if not checkcell.solved and cell != checkcell:
                    # Loop through all the possible values in the check cell
                    for pos in checkcell.possible:
                        # If we find a value that is in the source, remove it
                        if pos in possible:
                            possible.remove(pos)

            # If there is only one possible solution left, that must be the solution for this cell.
            if len(possible) == 1:
                cell.possible = possible.copy()
                change = cell.check_solved(change)
                if change:
                    return change

    return change


def int_check_column(colnum, sudoku, change):

    found = utils.check_values(sudoku.loc[:, colnum])

    for cell in sudoku.loc[:, colnum]:
        if not cell.solved:
            # Create a temporary list of possible values to check for
            possible = cell.possible.difference(found)

            # Loop through the other cells in the column to find their possible values
            for checkcell in sudoku.loc[:, colnum]:
                # Only check if the cell isn't solved and it isn't the cell we are comparing to
                if not checkcell.solved and cell != checkcell:
                    # Loop through all the possible values in the check cell
                    for pos in checkcell.possible:
                        # If we find a value that is in the source, remove it
                        if pos in possible:
                            possible.remove(pos)

            # If there is only one possible solution left, that must be the solution for this cell.
            if len(possible) == 1:
                cell.possible = possible.copy()
                change = cell.check_solved(change)
                if change:
                    return change

    return change


def int_check_quad(quad, sudoku, change):

    # Slice the board into the correct quadrant
    quadrant = utils.get_quad(quad, sudoku)

    found = utils.check_values_quad(quadrant)

    # Start checking the cells in the quadrant
    for row in quadrant.itertuples(index=False):
        for cell in row:
            if not cell.solved:
                # Create a tempoarty list of possible values to check for
                possible = cell.possible.difference(found)

                # Loop through the other cells in the quardrant to find their possible values
                for checkrow in quadrant.itertuples(index=False):
                    # Only check if the cell isn't solved and it isn't the cell we are comparing to
                    for checkcell in checkrow:

                        # Only check if the cell isn't solved and it isn't the cell we are comparing to
                        if not checkcell.solved and cell != checkcell:
                            for pos in checkcell.possible:
                                # If there is a value that is in the source possible list, remove it
                                if pos in possible:
                                    possible.remove(pos)

                # If there is only one possible solution left, that must be the solution for this cell
                if len(possible) == 1:
                    cell.possible = possible.copy()
                    change = cell.check_solved(change)
                    if change:
                        return change

    return change


def cross_check(sudoku, change):
    # Cross checks will compare the solution state of rows, columns, and quadrants to remove possible values
    for i in range(9):
        change = quad_to_row_check(i, sudoku, change)
        if change:
            return change
    for i in range(9):
        change = quad_to_col_check(i, sudoku, change)
        if change:
            return change
    for i in range(9):
        change = row_to_quad_check(i, sudoku, change)
        if change:
            return change
    for i in range(9):
        change = col_to_quad_check(i, sudoku, change)
        if change:
            return change


def quad_to_row_check(quad, sudoku, change):
    # Determines if two rows are solved in a particular quadrant, the unsolved row must contain the missing values
    # Thus, you can remove these missing values from the cells located in this row in other quadrants

    quadrant = utils.get_quad(quad, sudoku)

    # Check to see if two rows are completed within the quad
    incomplete_rows = set()

    for i, local_row in enumerate(quadrant.itertuples(index=False)):
        row_complete = True
        for cell in local_row:
            if cell.value == 0:
                row_complete = False

        if not row_complete:
            incomplete_rows.add(i)

    if len(incomplete_rows) == 1:
        # Check which values to remove
        found = utils.check_values_quad(quadrant)
        remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)

        row = utils.eval_row(quad, incomplete_rows.pop())

        for cell in sudoku.loc[row]:
            if not cell.solved and cell.quad != quad:
                change = cell.assign_possible(remove_pos, change)

    return change


def quad_to_col_check(quad, sudoku, change):
    # Determines if two columns are solved in a particular quadrant, the unsolved columns must contain the missing values
    # Thus, you can remove these missing values from the cells located in this columns in other quadrants

    quadrant = utils.get_quad(quad, sudoku)

    incomplete_cols = set()

    for i, local_col in quadrant.iteritems():
        col_complete = True
        for cell in local_col.values:
            if cell.value == 0:
                col_complete = False

        if not col_complete:
            incomplete_cols.add(i)

    if len(incomplete_cols) == 1:
        found = utils.check_values_quad(quadrant)
        remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)

        column = incomplete_cols.pop()
        
        for cell in sudoku.loc[:, column]:
            if not cell.solved and cell.quad != quad:
                change = cell.assign_possible(remove_pos, change)

    return change


def row_to_quad_check(rownum, sudoku, change):
    # Determines, within a row, if 2 quadrants have been completed. If they have, the outstanding values in that row must be placed in the remaining
    # cells in the row. Thus it is not possible to place them in any other location in that quadrant.

    found = utils.check_values(sudoku.loc[rownum])

    # Only check if 6 or more values have been filled in, as any less means 2 quadrants couldn't have been solved
    if len(found) > 5:

        incompleted_quads = utils.eval_quads(sudoku.loc[rownum])

        if len(incompleted_quads) == 1:

            remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)
            quadrant = utils.get_quad(incompleted_quads.pop(), sudoku)

            for row in quadrant.itertuples(index=False):
                for cell in row:
                    if not cell.solved and cell.row != rownum:
                        change = cell.assign_possible(remove_pos, change)

    return change


def col_to_quad_check(colnum, sudoku, change):
    # Determines, within a column, if 2 quadrants have been completed. If they have, the outstanding values in that column must be placed in the remaining
    # cells in the column. Thus it is not possible to place them in any other location in that quadrant.

    found = utils.check_values(sudoku.loc[:, colnum])

    if len(found) > 5:

        incompleted_quads = utils.eval_quads(sudoku.loc[:, colnum])

        if len(incompleted_quads) == 1:

            remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)
            quadrant = utils.get_quad(incompleted_quads.pop(), sudoku)

            for column in quadrant.itertuples(index=False):
                for cell in column:
                    if not cell.solved and cell.column != colnum:
                        change = cell.assign_possible(remove_pos, change)

    return change


def compare_answer(sudoku, solution):
    # Function to compare the answer to the solved puzzle
    solved = True

    for rownum in range(9):
        for colnum in range(9):
            if sudoku.loc[rownum, colnum].value != solution.loc[rownum, colnum].value:
                solved = False

    return solved


def validate_answer(sudoku):
    # Function to validate the answer if the solution is not known

    solved = True

    solved = validate_rows(sudoku, solved)
    solved = validate_columns(sudoku, solved)
    solved = validate_quadrants(sudoku, solved)

    return solved


def validate_rows(sudoku, solved):

    for rownum in range(9):
        found = utils.check_values(sudoku.loc[rownum])
        if len(found) != 9:
            solved = False

    return solved


def validate_columns(sudoku, solved):

    for colnum in range(9):
        found = utils.check_values(sudoku.loc[:, colnum])
        if len(found) != 9:
            solved = False

    return solved


def validate_quadrants(sudoku, solved):

    for quad in range(9):
        quadrant = utils.get_quad(quad, sudoku)
        found = utils.check_values_quad(quadrant)
        if len(found) != 9:
            solved = False

    return solved
