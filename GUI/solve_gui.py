import pandas
from puzzle_gui import Box


# Basic checks compare the value of other boxes in the region. They remove all values found from the possible
# values of boxes in the region.

def basic_check(gui, sudoku, baschange):

    # Once one box is solved, break out of the loop so the GUI updates

    for i in range(9):
        baschange = bas_check_row(gui, i, sudoku, baschange)
        if baschange:
            return baschange
    for i in range(9):
        baschange = bas_check_column(gui, i, sudoku, baschange)
        if baschange:
            return baschange
    for i in range(9):
        baschange = bas_check_quad(gui, i, sudoku, baschange)
        if baschange:
            return baschange

    return baschange


def bas_check_row(gui, rownum, sudoku, baschange):

    # Check which values exist in the row
    found = check_values(gui, sudoku.loc[rownum])

    # Assign the possible values. Found values cannot be possible
    for box in sudoku.loc[rownum]:
        if not box.solved:
            baschange = box.assign_possible(gui, found, baschange)
            if baschange:
                return baschange

    return baschange


def bas_check_column(gui, colnum, sudoku, baschange):

    # Check which values exist in the column
    found = check_values(gui, sudoku.loc[:, colnum])

    # Assign the possible values. Found values cannot be possible
    for box in sudoku.loc[:, colnum]:
        if not box.solved:
            baschange = box.assign_possible(gui, found, baschange)
            if baschange:
                return baschange

    return baschange


def bas_check_quad(gui, quad, sudoku, baschange):
    # Slice the board into the correct quadrant
    quadrant = get_quad(quad, sudoku)

    # Check which values exist in the quadrant
    found = check_values_quad(gui, quadrant)

    # Assign the possible values. Found values cannot be possible
    for row in quadrant.itertuples(index=False):
        for box in row:
            if not box.solved:
                baschange = box.assign_possible(gui, found, baschange)
                if baschange:
                    return baschange

    return baschange

# Intermediate checks will check the possible values of the boxes in a region
# If only one box in a region has a specfic possible value, that can be considered solved


def intermediate_check(gui, sudoku, intchange):

    for i in range(9):
        intchange = int_check_row(gui, i, sudoku, intchange)
    for i in range(9):
        intchange = int_check_column(gui, i, sudoku, intchange)
    for i in range(9):
        intchange = int_check_quad(gui, i, sudoku, intchange)

    return intchange


def int_check_row(gui, rownum, sudoku, intchange):

    # Perform a basic check to update possible values
    found = check_values(gui, sudoku.loc[rownum])

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
                intchange = box.check_solved(gui, intchange)

    return intchange


def int_check_column(gui, colnum, sudoku, intchange):

    # Perform a basic check to update possible values
    found = check_values(gui, sudoku.loc[:, colnum])

    for box in sudoku.loc[:, colnum]:
        if not box.solved:
            # Create a temporary list of possible values to check for
            possible = box.possible.copy()
            # Remove any found values from temporary list
            for val in found:
                if val in possible:
                    possible.remove(val)

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
                intchange = box.check_solved(gui, intchange)

    return intchange


def int_check_quad(gui, quad, sudoku, intchange):

    # Slice the board into the correct quadrant
    quadrant = get_quad(quad, sudoku)

    # Perform a basic check to update possible values
    found = check_values_quad(gui, quadrant)

    # Start checking the boxes in the quadrant
    for row in quadrant.itertuples(index=False):
        for box in row:
            if not box.solved:
                # Create a tempoarty list of possible values to check for
                possible = box.possible.copy()
                # Remove any found values from temporary list
                for val in found:
                    if val in possible:
                        possible.remove(val)

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
                    intchange = box.check_solved(gui, intchange)

    return intchange

# Function to check the solved values in a row or column


def check_values(gui, region):
    # Loop through the loop to see which
    found = []
    for box in region:
        if box.value != 0:
            found.append(box.value)

    return set(found)

# Function to check the solved values in a quadrant


def check_values_quad(gui, quadrant):
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


def validate_answer(gui, sudoku):

    solved = True

    solved = validate_rows(gui, sudoku, solved)
    solved = validate_columns(gui, sudoku, solved)
    solved = validate_quadrants(gui, sudoku, solved)

    return solved


def validate_rows(gui, sudoku, solved):

    for rownum in range(9):
        found = check_values(gui, sudoku.loc[rownum])
        if len(found) != 9:
            solved = False

    return solved


def validate_columns(gui, sudoku, solved):

    for colnum in range(9):
        found = check_values(gui, sudoku.loc[:, colnum])
        if len(found) != 9:
            solved = False

    return solved


def validate_quadrants(gui, sudoku, solved):

    for quad in range(9):
        quadrant = get_quad(quad, sudoku)
        found = check_values_quad(gui, quadrant)
        if len(found) != 9:
            solved = False

    return solved
