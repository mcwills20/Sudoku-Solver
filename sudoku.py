from importlib import reload

import pandas as pd
import puzzle
import solve
reload(puzzle)
reload(solve)

# This file is the current testing ground. Will be staging point for final algorithm

sudoku = puzzle.build_sudoku(
    "040100050107003960520008000000000017000906800803050620090060543600080700250097100")

# Build the solution to double check. TO DO: Automatic verifier
solution = puzzle.build_sudoku(
    "346179258187523964529648371965832417472916835813754629798261543631485792254397186")

print("Inital sudoku is")
print(sudoku)

change = True

while change:
    change = False
    sudoku, change = solve.basic_check(sudoku, change)

    if not change:
        sudoku, change = solve.intermediate_check(sudoku, change)

    if solve.validate_answer(sudoku):
        change = False
        print("Solve completed successfully")
        print(sudoku)

if not solve.validate_answer(sudoku):
    print("Solve Failed")
    print(sudoku)
    print("Correct answer was")
    print(solution)
