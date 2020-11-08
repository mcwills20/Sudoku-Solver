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


def check_values(df):

    # Loop through the loop to see which
    found = []
    for box in df:
        if box.value != 0:
            found.append(box.value)

    return found
