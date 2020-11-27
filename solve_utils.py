

def eval_row(quad, local_row):
    # Used in cross check. Converts the local row in a quadrant to the absolute row of the entire puzzle.
    if 0 <= quad <= 2:
        return local_row
    elif 3 <= quad <= 5:
        return local_row + 3
    else:
        return local_row + 6


def eval_col(quad, local_col):
    # Used in cross check. Converts the local column in a quadrant to the absolute column of the entire puzzle. NOT USED
    if quad == 0 or quad == 3 or quad == 6:
        return local_col
    elif quad == 1 or quad == 4 or quad == 7:
        return local_col + 3
    else:
        return local_col + 6


def eval_quads(region):
    # Used in cross check. Takes when giving a region (row or column), this will check to make sure how much of that region
    # is solved in a particular quadrant. If there are still cells to be solved in a quadrant, this will return those quadrants

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


def check_values(region):
    # Function to check the solved values in a row or column
    found = set()
    for box in region:
        if box.value != 0:
            found.add(box.value)

    return found


def check_values_quad(quadrant):
    # Function to check the solved values in a quadrant
    found = []
    for row in quadrant.itertuples(index=False):
        for box in row:
            if box.value != 0:
                found.append(box.value)

    return set(found)


def get_quad(quad, sudoku):
    # Function to slice the Sudoku Puzzle into a quadrant
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


def color_red(region):

    for cell in region:
        cell.gui.color = [1, 0, 0, 1]

def color_green(region):

    for cell in region:
        cell.gui.color = [0, 1, 0, 1]

def color_red_quad(quadrant):
    for row in quadrant.itertuples(index = False):
        for cell in row:
            cell.gui.color = [1, 0, 0, 1]

def color_green_quad(quadrant):
    for row in quadrant.itertuples(index = False):
        for cell in row:
            cell.gui.color = [0, 1, 0, 1]