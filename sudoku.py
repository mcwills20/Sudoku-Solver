import imp

import pandas as pd
import puzzle
import solve
imp.reload(puzzle)

df = puzzle.build_sudoku("004300209005009001070060043006002087190007400050083000600000105003508690042910300")

print("Inital sudoku is")
print(df)

for i in range(9):
    df = solve.check_row(i, df)
    df = solve.check_column(i, df)

print("After one pass")
print(df)

