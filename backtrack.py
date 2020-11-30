import solve
import solve_utils as utils
import puzzle


def backtrack(sudoku, cellref, forward):

    cell = sudoku.loc[cellref]

    if cell.mutable:

        if cell.new:
            cell.tpossible = cell.possible.copy()
            cell.new = False

        if len(cell.tpossible) == 0:
            cell.new = True
            cell.value = 0
            cell.gui.backtrack_update(cell.value)
            return cell.previous, False

        safe, cell.value = bt_check(sudoku, cell, cell.tpossible.pop())

        cell.gui.backtrack_update(cell.value)

        if safe:
            return cell.next, True
            #backtrack(sudoku, cell.next)
        elif cell.new:
            cell.value = 0
            # cell.gui.backtrack_update(cell.value)
            # return cell.previous, False
        else:
            return (cell.row, cell.column), forward

    else:
        if forward or cellref == (0, 0):
            return cell.next, True,
        elif not forward:
            return cell.previous, False


def bt_check(sudoku, cell, value):
    safe = bt_check_row(sudoku, cell, value)
    if not safe:
        return safe, 0

    safe = bt_check_column(sudoku, cell, value)
    if not safe:
        return safe, 0

    safe = bt_check_quadrant(sudoku, cell, value)
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


def bt_check_quadrant(sudoku, cell, value):

    quadrant = utils.get_quad(cell.quad, sudoku)

    for row in quadrant.itertuples(index=False):
        for check in row:
            if check != cell and check.value != 0:
                if check.value == value:
                    return False

    return True
