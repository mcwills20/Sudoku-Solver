import imp

import pandas as pd
import puzzle
imp.reload(puzzle)

df = puzzle.build_puzzle("004300209005009001070060043006002087190007400050083000600000105003508690042910300")

print(df)