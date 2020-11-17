import puzzle_gui
import solve_gui

import time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

class SudokuCell(Button):
    def __init__(self, **kwargs):
        super(SudokuCell, self).__init__(**kwargs)

class SudokuPy(App):

    def __init__(self, sudoku, **kwargs):
        super(SudokuPy, self).__init__(**kwargs)
        self.sudoku = sudoku

    def build(self):

        # The main window
        root_widget = BoxLayout(orientation='vertical')

        # Begin building the sudoku grid
        puzzle = GridLayout(cols=9, size_hint_y=10)
        for rownum in range(9):
            for box in sudoku.loc[rownum]:
                if box.value != 0:
                    puzzle.add_widget(SudokuCell(text=str(box.value)))
                else:
                    puzzle.add_widget(SudokuCell(text=''))

        # Store a reference to the cells for easy manipulation later
        self.cell_list = puzzle.children

        # Build the window
        root_widget.add_widget(TextInput(text='Sudoku', size_hint_y=1))
        root_widget.add_widget(puzzle)
        root_widget.add_widget(
            Button(text='Solve', on_release=self.solve_sudoku))

        # Store a reference to the textinput for easy manipulation later
        self.textinput = root_widget.children[-1]

        return root_widget

    # When solved button is press, create an event to cycle through the basic solutions
    def solve_sudoku(self, event):
        self.basicsolve = Clock.schedule_interval(self.solve_step, 0.1)

    def solve_step(self, dt):
        # Erase any background colors left over
        self.clear_format()
        _change = False
        _change = solve_gui.basic_check(self, self.sudoku, _change)

        # If nothing changed, validate the answer
        if not _change:
            if solve_gui.validate_answer(self, sudoku):
                self.on_complete()
                self.basicsolve.cancel()
            else:
                _change = solve_gui.intermediate_check(self, self.sudoku, _change)
                if not _change:
                    self.on_fail()
                    self.basicsolve.cancel()

    def clear_format(self):
        _color = [1, 1, 1, 1]
        for box in self.cell_list:
            box.background_color = _color

    def on_complete(self):
        for box in self.cell_list:
            box.background_color = [0, 1, 0, 1]
        self.textinput.text = 'SOLVED'

    def on_fail(self):
        for box in self.cell_list:
            box.background_color = [1, 0, 0, 1]
        self.textinput.text = 'FAILED'

        
sudoku = puzzle_gui.build_sudoku(
    "200000001003060008807031940002506070409800056100000380038670500705090263000004000")

if __name__ == '__main__':
    SudokuPy(sudoku).run()
