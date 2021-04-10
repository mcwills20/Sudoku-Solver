import sudoku
import gui


if __name__ == '__main__':

    blank = sudoku.Sudoku(
        "000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    gui.SudokuPy(blank).run()
