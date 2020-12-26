## Sudoku-Solver
This is my implementation of a Sudoku solver with a graphical user interface. It allows the user to enter in a puzzle as a string, load it into the program, and solve it using a set of basic solving algorithms, backtracking, or manual solution entry.

## Motivation
This project was created as a learning exercise with several goals in mind:

First was to familiarize myself with creating a GUI in Python. I have worked with Python in the past but only have done very simple graphical interfaces. I wanted to learn a GUI framework (for this instance, I chose Kivy) and practice managing a more complex interface.

Second, I wanted to get more comfortable working with Pandas dataframes. In my previous projects using Pandas, I was never fully understood methods such as .loc[] and .itertuples(). By creating a Sudoku solver, I got much more experience with slicing and iterating through dataframe rows, columns, and smaller subsections (such as boxes) of the dataframe.

Finally, learning version control using Git was a priority. I had only ever used crude forms of version control in the past: learning the Git workflow helped greatly in managing the code base and gave me confidence to try more radical refactoring solutions.


## How To Use
Upon loading the program, there will be a blank Sudoku grid. You can manually build a puzzle using the "Pen" tool located on the right hand side by selecting which number to input and clicking on a cell to assign that value. You can also enter in an 81 character long string of integers into the text entry box on the top of the program and selecting "Build" to load the puzzle into the program. The proper format for this string is going left to right, entering each known value, with 0 being entered if blank.

From here you can use the Pen and Pencil tool to manually solve the puzzle. Pen will enter the selected value as an answer, Pencil will leave a reminder of the selected value in the cell. Note that the Pen tool's answers will be retained while performing the Smart Solve and Backtrack Solve functions, but the Pencil tool's reminders will not be.

Pressing the Smart Solve button will perform an algorithm of some basic Sudoku solving techniques to eliminate possible values from the cells and assigning answers when able. If this algorithm fails, or if you do not wish to use this algorithm, the Backtrack Solve will perform a backtracking algorithm to brute force the correct answer if one exists. This method is much slower than the smart solve algorithm, and it is recommended to run the Smart Solve first to eliminate possibile values that the backtrack needs to check, as the information from the Smart Solve will be retained. This will substaintially reduce the time needed to solve.

After a puzzle is solved, you can build another puzzle using the text entry at the top of the screen, which will reitialize the board and allow you to work on another puzzle.


## Credits
Thank you to Kyubyong Park from Kaggle for uploading a data set of Sudoku puzzles

https://www.kaggle.com/bryanpark/sudoku