from importlib import reload

import pandas as pd
import puzzle
import solve
reload(puzzle)
reload(solve)

# This file is the current testing ground. Will be staging point for final algorithm

sudoku = puzzle.build_sudoku(
    "200000001003060008807031940002506070409800056100000380038670500705090263000004000")

print("Inital sudoku is")
print(sudoku)

change = True

while change:
    change = False
    change = solve.basic_check(sudoku, change)

    if not change:
        change = solve.intermediate_check(sudoku, change)

    if solve.validate_answer(sudoku):
        change = False
        print("Solve completed successfully")
        print(sudoku)

if not solve.validate_answer(sudoku):
    print("Solve Failed")
    print(sudoku)
