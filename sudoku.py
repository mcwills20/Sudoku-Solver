from importlib import reload

import pandas as pd
import puzzle
import solve
reload(puzzle)
reload(solve)

# This file is the current testing ground. Will be staging point for final algorithm

df = puzzle.build_sudoku(
    "004300209005009001070060043006002087190007400050083000600000105003508690042910300")

print("Inital sudoku is")
print(df)

# Do a first pass with the simple check algorithms
for i in range(9):
    df = solve.check_row(i, df)
    df = solve.check_column(i, df)
    df = solve.check_quad(i, df)

# Print the results
print("After one pass")
print(df)

# Build the solution to double check. TO DO: Automatic verifier
solved = puzzle.build_sudoku(
    "864371259325849761971265843436192587198657432257483916689734125713528694542916378")
print("The solved puzzle should be")
print(solved)
