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
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ListProperty


class SudokuCell(GridLayout):

    color = ListProperty([1, 1, 1, 1])

    def __init__(self, value, possible, **kwargs):
        super(SudokuCell, self).__init__(**kwargs)

        if value == '0':

            self.possible = possible

        else:
            self.update_solution(value)
            # Turn the background color back to white
            self.color = [1, 1, 1, 1]

    def update_possible(self, possible):

        self.possible = possible

        if 1 in self.possible:
            self.ids.pos1.text = '1'
        else:
            self.ids.pos1.text = ''

        if 2 in self.possible:
            self.ids.pos2.text = '2'
        else:
            self.ids.pos2.text = ''

        if 3 in self.possible:
            self.ids.pos3.text = '3'
        else:
            self.ids.pos3.text = ''

        if 4 in self.possible:
            self.ids.pos4.text = '4'
        else:
            self.ids.pos4.text = ''

        if 5 in self.possible:
            self.ids.pos5.text = '5'
        else:
            self.ids.pos5.text = ''

        if 6 in self.possible:
            self.ids.pos6.text = '6'
        else:
            self.ids.pos6.text = ''

        if 7 in self.possible:
            self.ids.pos7.text = '7'
        else:
            self.ids.pos7.text = ''

        if 8 in self.possible:
            self.ids.pos8.text = '8'
        else:
            self.ids.pos8.text = ''

        if 9 in self.possible:
            self.ids.pos9.text = '9'
        else:
            self.ids.pos9.text = ''

    def update_solution(self, value):
        self.possible = []
        self.update_possible(self.possible)
        self.ids.pos5.text = str(value)
        self.ids.pos5.font_size = 25
        self.ids.pos5.color = [0, 0, 0, 1]
        self.color = [0, 1, 0, 1]


class QuadrantGrid(GridLayout):
    def __init__(self, **kwargs):
        super(QuadrantGrid, self).__init__(**kwargs)


class SudokuGrid(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuGrid, self).__init__(**kwargs)


class SudokuPy(App):

    def __init__(self, sudoku, **kwargs):
        super(SudokuPy, self).__init__(**kwargs)
        self.sudoku = sudoku
        self.cell_list = []

    def build(self):

        # The main window
        root_widget = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # Begin building the sudoku grid
        puzzle = SudokuGrid(size_hint=(1, .7))
        for quad in range(9):
            puzzle.add_widget(self.build_quad(quad))

        # Build the window
        root_widget.add_widget(TextInput(text='Sudoku', size_hint=(1, .1)))
        root_widget.add_widget(puzzle)
        root_widget.add_widget(
            Button(text='Solve', on_release=self.solve_sudoku, size_hint=(1, .05)))
        root_widget.add_widget(
            Button(text='Test', on_release=self.test, size_hint=(1, .05)))

        # Store a reference to the textinput for easy manipulation later
        self.textinput = root_widget.children[-1]

        return root_widget

    def build_quad(self, quadnum):
        quadrant = solve_gui.get_quad(quadnum, self.sudoku)

        grid = QuadrantGrid()

        for _row in quadrant.itertuples(index=False):
            for cell in _row:
                cell.gui = SudokuCell(
                    value=str(cell.value), possible=cell.possible)
                grid.add_widget(cell.gui)
                self.cell_list.append(cell.gui)

        return grid

    # When solved button is press, create an event to cycle through the basic solutions

    def solve_sudoku(self, event):
        self.basicsolve = Clock.schedule_interval(self.solve_step, 0.3)

    def solve_step(self, dt):
        # Erase any background colors left over
        self.clear_format()
        change = False
        change = solve_gui.basic_check(self.sudoku, change)

        # If nothing changed, validate the answer
        if not change:
            if solve_gui.validate_answer(self.sudoku):
                self.on_complete()
                self.basicsolve.cancel()
            else:
                change = solve_gui.intermediate_check(
                    self.sudoku, change)
                if not change:
                    #change = solve_gui.cross_check(self.sudoku, change)
                    if not change:
                        self.on_fail()
                        self.basicsolve.cancel()

    def clear_format(self):
        color = [1, 1, 1, 1]
        for cell in self.cell_list:
            cell.color = color

    def on_complete(self):
        for cell in self.cell_list:
            cell.color = [0, 1, 0, 1]
        self.textinput.text = 'SOLVED'

    def on_fail(self):
        for cell in self.cell_list:
            cell.color = [1, 0, 0, 1]
        self.textinput.text = 'FAILED'

    def test(self, event):
        change = solve_gui.row_to_quad_check(0, self.sudoku, True)
        print('test')

# sudoku = puzzle_gui.build_sudoku(
#    "200000001003060008807031940002506070409800056100000380038670500705090263000004000")


sudoku = puzzle_gui.build_sudoku(
    "123456700000000000000000000000000000000000000000000000000000000000000000000000000")

if __name__ == '__main__':
    SudokuPy(sudoku).run()
