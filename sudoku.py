import imp

import pandas as pd
import puzzle
imp.reload(puzzle)

row1 = [0,0,8,1,9,0,3,4,0]
row2 = [3,0,2,6,4,0,0,0,9]
row3 = [4,9,0,0,0,0,0,0,7]
row4 = [9,0,0,0,5,0,4,0,0]
row5 = [0,0,6,0,8,0,9,0,0]
row6 = [0,0,3,0,6,0,0,0,1]
row7 = [1,0,0,0,0,0,0,2,6]
row8 = [7,0,0,0,1,6,8,0,3]
row9 = [0,6,9,0,3,5,7,0,0]

tlist= [row1,row2,row3,row4,row5,row6,row7,row8,row9]

df = pd.DataFrame(tlist)

row1test = []
for i, val in enumerate(row1):
    row1test.append(puzzle.box(val,1,i))
print(row1test)