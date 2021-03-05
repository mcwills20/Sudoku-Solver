import solve_utils as utils


def backtrack(sudoku, cellref, forward):

    cell = sudoku.loc[cellref]

    if cell.mutable:

        # Create a non destructive copy of the possible list to cycle through during backtracking
        if cell.new:
            cell.tpossible = cell.possible.copy()
            cell.new = False

        # Items are removed from temp set while being used. If all are used, the current state of the sudoku solve is not possible
        # So the algorithm needs to go back to modify the previous value
        if len(cell.tpossible) == 0:
            cell.new = True
            cell.value = 0
            cell.gui.backtrack_update(cell.value)
            return cell.previous, False

        safe, cell.value = bt_check(sudoku, cell, cell.tpossible.pop())

        cell.gui.backtrack_update(cell.value)

        # If value is safely placed, go to the next cell
        if safe:
            return cell.next, True
        # If a value was not placed, repeat the cell
        else:
            return (cell.row, cell.column), forward

    else:
        # If the cell is not mutable, go in the direction of the last call
        if forward:
            return cell.next, True,
        else:
            return cell.previous, False


def bt_check(sudoku, cell, value):

    # All checks see if it is safe to place a value. If not, return that it is not and a value of 0.
    safe = bt_check_row(sudoku, cell, value)
    if not safe:
        return safe, 0

    safe = bt_check_column(sudoku, cell, value)
    if not safe:
        return safe, 0

    safe = bt_check_box(sudoku, cell, value)
    if not safe:
        return safe, 0
    else:
        return safe, value


def bt_check_row(sudoku, cell, value):

    for check in sudoku.loc[cell.row]:

        if check != cell and check.value != 0:
            if check.value == value:
                return False

    return True


def bt_check_column(sudoku, cell, value):

    for check in sudoku.loc[:, cell.column]:

        if check != cell and check.value != 0:
            if check.value == value:
                return False

    return True


def bt_check_box(sudoku, cell, value):

    box = utils.get_box(cell.box, sudoku)

    for check in utils.iter_box(box):
        if check != cell and check.value != 0:
            if check.value == value:
                return False

    return True
