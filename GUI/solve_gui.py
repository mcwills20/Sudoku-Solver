import pandas
from puzzle_gui import Box


# Basic checks compare the value of other boxes in the region. They remove all values found from the possible
# values of boxes in the region.

def basic_check(sudoku, change):

    # Once one box is solved, break out of the loop so the GUI updates

    for i in range(9):
        change = bas_check_row(i, sudoku, change)
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
    found = check_values(sudoku.loc[rownum])

    # Assign the possible values. Found values cannot be possible
    for box in sudoku.loc[rownum]:
        if not box.solved:
            change = box.assign_possible(found, change)
            if change:
                return change

    return change


def bas_check_column(colnum, sudoku, change):

    # Check which values exist in the column
    found = check_values(sudoku.loc[:, colnum])

    # Assign the possible values. Found values cannot be possible
    for box in sudoku.loc[:, colnum]:
        if not box.solved:
            change = box.assign_possible(found, change)
            if change:
                return change

    return change


def bas_check_quad(quad, sudoku, change):
    # Slice the board into the correct quadrant
    quadrant = get_quad(quad, sudoku)

    # Check which values exist in the quadrant
    found = check_values_quad(quadrant)

    # Assign the possible values. Found values cannot be possible
    for row in quadrant.itertuples(index=False):
        for box in row:
            if not box.solved:
                change = box.assign_possible(found, change)
                if change:
                    return change

    return change

# Intermediate checks will check the possible values of the boxes in a region
# If only one box in a region has a specfic possible value, that can be considered solved


def intermediate_check(sudoku, change):

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


def cross_check(sudoku, change):
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


def int_check_row(rownum, sudoku, change):

    found = check_values(sudoku.loc[rownum])

    for box in sudoku.loc[rownum]:
        if not box.solved:
            # Create a temporary list of possible values to check for
            possible = box.possible.copy()
            # Remove any found values from temporary list
            for val in found:
                if val in possible:
                    possible.remove(val)

            # Loop through the other boxes in the row to find their possible values
            for checkbox in sudoku.loc[rownum]:
                # Only check if the box isn't solved and it isn't the box we are comparing to
                if not checkbox.solved and box != checkbox:
                    # Loop through all the possible values in the check box
                    for pos in checkbox.possible:
                        # If we find a value that is in the source, remove it
                        if pos in possible:
                            possible.remove(pos)

            # If there is only one possible solution left, that must be the solution for this box.
            if len(possible) == 1:
                box.possible = possible.copy()
                change = box.check_solved(change)
                if change:
                    return change

    return change


def int_check_column(colnum, sudoku, change):

    found = check_values(sudoku.loc[:, colnum])

    for box in sudoku.loc[:, colnum]:
        if not box.solved:
            # Create a temporary list of possible values to check for
            possible = box.possible.difference(found)

            # Loop through the other boxes in the column to find their possible values
            for checkbox in sudoku.loc[:, colnum]:
                # Only check if the box isn't solved and it isn't the box we are comparing to
                if not checkbox.solved and box != checkbox:
                    # Loop through all the possible values in the check box
                    for pos in checkbox.possible:
                        # If we find a value that is in the source, remove it
                        if pos in possible:
                            possible.remove(pos)

            # If there is only one possible solution left, that must be the solution for this box.
            if len(possible) == 1:
                box.possible = possible.copy()
                change = box.check_solved(change)
                if change:
                    return change

    return change


def int_check_quad(quad, sudoku, change):

    # Slice the board into the correct quadrant
    quadrant = get_quad(quad, sudoku)

    found = check_values_quad(quadrant)

    # Start checking the boxes in the quadrant
    for row in quadrant.itertuples(index=False):
        for box in row:
            if not box.solved:
                # Create a tempoarty list of possible values to check for
                possible = box.possible.difference(found)

                # Loop through the other boxes in the quardrant to find their possible values
                for checkrow in quadrant.itertuples(index=False):
                    # Only check if the box isn't solved and it isn't the box we are comparing to
                    for checkbox in checkrow:

                        # Only check if the box isn't solved and it isn't the box we are comparing to
                        if not checkbox.solved and box != checkbox:
                            for pos in checkbox.possible:
                                # If there is a value that is in the source possible list, remove it
                                if pos in possible:
                                    possible.remove(pos)

                # If there is only one possible solution left, that must be the solution for this box
                if len(possible) == 1:
                    box.possible = possible.copy()
                    change = box.check_solved(change)
                    if change:
                        return change

    return change

# Determines if two rows are solved in a particular quadrant, the unsolved row must contain the missing values
# Thus, you can remove these missing values from the cells located in this row in other quadrants


def quad_to_row_check(quad, sudoku, change):

    quadrant = get_quad(quad, sudoku)

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
        found = check_values_quad(quadrant)
        remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)

        row = eval_row(quad, incomplete_rows.pop())

        for cell in sudoku.loc[row]:
            if not cell.solved and cell.quad != quad:
                change = cell.assign_possible(remove_pos, change)

    return change

# Determines if two columns are solved in a particular quadrant, the unsolved columns must contain the missing values
# Thus, you can remove these missing values from the cells located in this columns in other quadrants


def quad_to_col_check(quad, sudoku, change):

    quadrant = get_quad(quad, sudoku)

    incomplete_cols = set()

    for i, local_col in quadrant.iteritems():
        col_complete = True
        for cell in local_col.values:
            if cell.value == 0:
                col_complete = False

        if not col_complete:
            incomplete_cols.add(i)

    if len(incomplete_cols) == 1:
        found = check_values_quad(quadrant)
        remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)

        column = eval_col(quad, incomplete_cols.pop())

        for cell in sudoku.loc[:, column]:
            if not cell.solved and cell.quad != quad:
                change = cell.assign_possible(remove_pos, change)

    return change

# Determines, within a row, if 2 quadrants have been completed. If they have, the outstanding values in that row must be placed in the remaining
# cells in the row. Thus it is not possible to place them in any other location in that quadrant.


def row_to_quad_check(rownum, sudoku, change):

    found = check_values(sudoku.loc[rownum])

    # Only check if 6 or more values have been filled in, as any less means 2 quadrants couldn't have been solved
    if len(found) > 5:

        incompleted_quads = eval_quads(sudoku.loc[rownum])

        if len(incompleted_quads) == 1:

            remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)
            quadrant = get_quad(incompleted_quads.pop(), sudoku)

            for row in quadrant.itertuples(index=False):
                for box in row:
                    if not box.solved and box.row != rownum:
                        change = box.assign_possible(remove_pos, change)

    return change


def col_to_quad_check(colnum, sudoku, change):

    found = check_values(sudoku.loc[:, colnum])

    if len(found) > 5:

        incompleted_quads = eval_quads(sudoku.loc[:, colnum])

        if len(incompleted_quads) == 1:

            remove_pos = {1, 2, 3, 4, 5, 6, 7, 8, 9}.difference(found)
            quadrant = get_quad(incompleted_quads.pop(), sudoku)

            for column in quadrant.itertuples(index=False):
                for box in column:
                    if not box.solved and box.column != colnum:
                        change = box.assign_possible(remove_pos, change)

    return change


def eval_row(quad, local_row):

    if 0 <= quad <= 2:
        return local_row
    elif 3 <= quad <= 5:
        return local_row + 3
    else:
        return local_row + 6


def eval_col(quad, local_col):

    if quad == 0 or quad == 3 or quad == 6:
        return local_col
    elif quad == 1 or quad == 4 or quad == 7:
        return local_col + 3
    else:
        return local_col + 6


def eval_quads(region):

    quad_loop = 0
    quad_complete = True

    incompleted_quads = set()

    for cell in region:
        quad_loop += 1
        if cell.value == 0:
            quad_complete = False

        # Reset the internal quad loop to tell that we will enter another quadrant on the next cell
        if quad_loop == 3:

            if not quad_complete:
                incompleted_quads.add(cell.quad)

            quad_loop = 0
            quad_complete = True

    return incompleted_quads


# Function to check the solved values in a row or column
def check_values(region):
    # Loop through the loop to see which
    found = []
    for box in region:
        if box.value != 0:
            found.append(box.value)

    return set(found)

# Function to check the solved values in a quadrant


def check_values_quad(quadrant):
    found = []
    for row in quadrant.itertuples(index=False):
        for box in row:
            if box.value != 0:
                found.append(box.value)

    return set(found)

# Function to slice the Sudoku Puzzle into a quadrant


def get_quad(quad, sudoku):
    if quad == 0:
        return sudoku.loc[0:2, 0:2]
    elif quad == 1:
        return sudoku.loc[0:2, 3:5]
    elif quad == 2:
        return sudoku.loc[0:2, 6:8]
    elif quad == 3:
        return sudoku.loc[3:5, 0:2]
    elif quad == 4:
        return sudoku.loc[3:5, 3:5]
    elif quad == 5:
        return sudoku.loc[3:5, 6:8]
    elif quad == 6:
        return sudoku.loc[6:8, 0:2]
    elif quad == 7:
        return sudoku.loc[6:8, 3:5]
    elif quad == 8:
        return sudoku.loc[6:8, 6:8]

# Function to compare the answer to the solved puzzle


def compare_answer(sudoku, solution):

    solved = True

    for rownum in range(9):
        for colnum in range(9):
            if sudoku.loc[rownum, colnum].value != solution.loc[rownum, colnum].value:
                solved = False

    return solved

# Function to validate the answer if the solution is not known


def validate_answer(sudoku):

    solved = True

    solved = validate_rows(sudoku, solved)
    solved = validate_columns(sudoku, solved)
    solved = validate_quadrants(sudoku, solved)

    return solved


def validate_rows(sudoku, solved):

    for rownum in range(9):
        found = check_values(sudoku.loc[rownum])
        if len(found) != 9:
            solved = False

    return solved


def validate_columns(sudoku, solved):

    for colnum in range(9):
        found = check_values(sudoku.loc[:, colnum])
        if len(found) != 9:
            solved = False

    return solved


def validate_quadrants(sudoku, solved):

    for quad in range(9):
        quadrant = get_quad(quad, sudoku)
        found = check_values_quad(quadrant)
        if len(found) != 9:
            solved = False

    return solved
