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
    for box in sudoku.loc[colnum]:
        if not box.solved:
            box.assign_possible(_found)

    return sudoku


def check_quad(box, sudoku):
    pass


def check_values(df):

    # Loop through the loop to see which
    found = []
    for box in df:
        if box.value != 0:
            found.append(box.value)

    return found
