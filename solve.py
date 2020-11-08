import pandas
from puzzle import Box


def check_row(rownum, sudoku):

    # Check to see which values exist in the row
    _found = check_values(sudoku.loc[rownum])

    # Assign the possible values. Found values cannot be possible
    for box in sudoku.loc[rownum]:
        if not box.solved:
            box.assign_possible(_found)

    return sudoku


def check_column(colnum, sudoku):

    # Store the current column as a temporary df
    _found = check_values(sudoku.loc[:, colnum])

    # Assign the possible values. Found values cannot be possible
    for box in sudoku.loc[:, colnum]:
        if not box.solved:
            box.assign_possible(_found)

    return sudoku


def check_quad(quad, sudoku):

    # Get the current quadrant
    if quad == 0:
        _quadrant = sudoku.loc[0:2, 0:2]
    elif quad == 1:
        _quadrant = sudoku.loc[0:2, 3:5]
    elif quad == 2:
        _quadrant = sudoku.loc[0:2, 6:8]
    elif quad == 3:
        _quadrant = sudoku.loc[3:5, 0:2]
    elif quad == 4:
        _quadrant = sudoku.loc[3:5, 3:5]
    elif quad == 5:
        _quadrant = sudoku.loc[3:5, 6:8]
    elif quad == 6:
        _quadrant = sudoku.loc[6:8, 0:2]
    elif quad == 7:
        _quadrant = sudoku.loc[6:8, 3:5]
    elif quad == 8:
        _quadrant = sudoku.loc[6:8, 6:8]

    # Loop through the quadrant to find the values
    # Because it is structured different, cannot use check_values()
    _found = []
    for _row in _quadrant.itertuples(index=False):
        for box in _row:
            if box.value != 0:
                _found.append(box.value)

    # Assign the possible values. Found values cannot be possible
    for _row in _quadrant.itertuples(index=False):
        for box in _row:
            if not box.solved:
                box.assign_possible(_found)

    return sudoku

# Intermediate checks will check the possible values of the boxes in a region
# If only one box in a region has a specfic possible value, that can be considered solved
def int_check_row(rownum, sudoku):

    # Perform a basic check to update possible values
    _found = check_values(sudoku.loc[rownum])

    for box in sudoku.loc[rownum]:
        if not box.solved:
            # Create a temporary list of possible values to check for
            _possible = box.possible.copy()
            # Remove any found values from temporary list
            for val in _found:
                if val in _possible:
                    _possible.remove(val)

            # Loop through the other boxes in the row to find their possible values
            for checkbox in sudoku.loc[rownum]:
                # Only check if the box isn't solved and it isn't the box we are comparing to
                if not checkbox.solved and box != checkbox:
                    # Loop through all the possible values in the check box
                    for _pos in checkbox.possible:
                        # If we find a value that is in the source, remove it
                        if _pos in _possible:
                            _possible.remove(_pos)

            # If there is only one possible solution left, that must be the solution for this box.
            if len(_possible) == 1:
                box.possible = _possible
                box.check_solved()

    return sudoku

def int_check_column(colnum, sudoku):
    
    # Perform a basic check to update possible values
    _found = check_values(sudoku.loc[:,colnum])

    for box in sudoku.loc[:,colnum]:
        if not box.solved:
            # Create a temporary list of possible values to check for
            _possible = box.possible.copy()
            # Remove any found values from temporary list
            for val in _found:
                if val in _possible:
                    _possible.remove(val)

            # Loop through the other boxes in the row to find their possible values
            for checkbox in sudoku.loc[:,colnum]:
                # Only check if the box isn't solved and it isn't the box we are comparing to
                if not checkbox.solved and box != checkbox:
                    # Loop through all the possible values in the check box
                    for _pos in checkbox.possible:
                        # If we find a value that is in the source, remove it
                        if _pos in _possible:
                            _possible.remove(_pos)

            # If there is only one possible solution left, that must be the solution for this box.
            if len(_possible) == 1:
                box.possible = _possible
                box.check_solved()

    return sudoku


    
# Function to check the solved values in a region
def check_values(df):
    # Loop through the loop to see which
    found = []
    for box in df:
        if box.value != 0:
            found.append(box.value)

    return found

# Function to slice the Sudoku Puzzle into a quadrant
def get_quad(quad, df):
    pass

