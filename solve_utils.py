

def eval_row(boxnum, local_row):
    # Used in cross check. Converts the local row in a box to the absolute row of the entire puzzle.
    if 0 <= boxnum <= 2:
        return local_row
    elif 3 <= boxnum <= 5:
        return local_row + 3
    else:
        return local_row + 6


def eval_col(boxnum, local_col):
    # Used in cross check. Converts the local column in a box to the absolute column of the entire puzzle. NOT USED
    if boxnum == 0 or boxnum == 3 or boxnum == 6:
        return local_col
    elif boxnum == 1 or boxnum == 4 or boxnum == 7:
        return local_col + 3
    else:
        return local_col + 6


def eval_boxes(region):
    # Used in cross check. Takes when giving a region (row or column), this will check to make sure how much of that region
    # is solved in a particular box. If there are still cells to be solved in a box, this will return those boxess

    box_loop = 0
    box_complete = True

    incompleted_boxes = set()

    for cell in region:
        box_loop += 1
        if cell.value == 0:
            box_complete = False

        # Reset the internal box loop to tell that we will enter another box on the next cell
        if box_loop == 3:

            if not box_complete:
                incompleted_boxes.add(cell.box)

            box_loop = 0
            box_complete = True

    return incompleted_boxes


def check_values(region):
    # Function to check the solved values in a row or column
    found = set()
    for cell in region:
        if cell.value != 0:
            found.add(cell.value)

    return found


def check_values_box(box):
    # Function to check the solved values in a box
    found = []
    for row in box.itertuples(index=False):
        for cell in row:
            if cell.value != 0:
                found.append(cell.value)

    return set(found)


def get_box(boxnum, sudoku):
    # Function to slice the Sudoku Puzzle into a box
    if boxnum == 0:
        return sudoku.loc[0:2, 0:2]
    elif boxnum == 1:
        return sudoku.loc[0:2, 3:5]
    elif boxnum == 2:
        return sudoku.loc[0:2, 6:8]
    elif boxnum == 3:
        return sudoku.loc[3:5, 0:2]
    elif boxnum == 4:
        return sudoku.loc[3:5, 3:5]
    elif boxnum == 5:
        return sudoku.loc[3:5, 6:8]
    elif boxnum == 6:
        return sudoku.loc[6:8, 0:2]
    elif boxnum == 7:
        return sudoku.loc[6:8, 3:5]
    elif boxnum == 8:
        return sudoku.loc[6:8, 6:8]


def color_red(region):

    for cell in region:
        cell.gui.color = [1, 0, 0, 1]

def color_green(region):

    for cell in region:
        cell.gui.color = [0, 1, 0, 1]

def color_red_box(box):
    for row in box.itertuples(index = False):
        for cell in row:
            cell.gui.color = [1, 0, 0, 1]

def color_green_box(box):
    for row in box.itertuples(index = False):
        for cell in row:
            cell.gui.color = [0, 1, 0, 1]

def entry_generator(entry):
    for i in range(81):
        yield entry[i]