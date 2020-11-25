import puzzle
import solve
import solve_utils as utils

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
from kivy.uix.behaviors import ButtonBehavior


class SudokuCell(ButtonBehavior, GridLayout):

    color = ListProperty([1, 1, 1, 1])

    def __init__(self, cell, **kwargs):
        super(SudokuCell, self).__init__(**kwargs)

        self.cell = cell
        if self.cell.value == 0:

            self.possible = self.cell.possible
            self.man_possible = set()

        else:
            self.update_solution(self.cell.value)
            # Turn the background color back to white
            self.color = [1, 1, 1, 1]

    def update_possible(self, possible):

        self.possible = possible

        for position, labelid in enumerate(self.ids, 1):
            if position in self.possible:
                self.ids[labelid].text = str(position)
            else:
                self.ids[labelid].text = ''

    def update_solution(self, value):
        self.update_possible(set())
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


class ManualInput(BoxLayout):
    def __init__(self, **kwargs):
        super(ManualInput, self).__init__(**kwargs)


class SudokuPy(App):

    def __init__(self, sudoku, **kwargs):
        super(SudokuPy, self).__init__(**kwargs)
        self.sudoku = sudoku
        self.cell_list = []
        self.pen = False
        self.pencil = False
        self.entry = ''

    def build(self):

        # The main window
        root_widget = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # Build main puzzle interface

        interface = BoxLayout(orientation='horizontal', size_hint=(1, .7))

        # Build the sudoku grid and add it to the interface
        puzzle = SudokuGrid(size_hint=(3.5, 1))
        for quad in range(9):
            puzzle.add_widget(self.build_quad(quad))
        interface.add_widget(puzzle)

        # Add the manual buttons
        interface.add_widget(ManualInput())

        # Build the window
        root_widget.add_widget(TextInput(text='Sudoku', size_hint=(1, .1)))
        root_widget.add_widget(interface)
        root_widget.add_widget(
            Button(text='Solve', on_release=self.solve_sudoku, size_hint=(1, .05)))
        root_widget.add_widget(
            Button(text='Test', on_release=self.test, size_hint=(1, .05)))

        # Store a reference to the textinput for easy manipulation later
        self.textinput = root_widget.children[-1]

        return root_widget

    def build_quad(self, quadnum):
        quadrant = utils.get_quad(quadnum, self.sudoku)

        grid = QuadrantGrid()

        for _row in quadrant.itertuples(index=False):
            for cell in _row:
                cell.gui = SudokuCell(cell)
                grid.add_widget(cell.gui)
                self.cell_list.append(cell.gui)

        return grid

    # When solved button is press, create an event to cycle through the basic solutions

    def solve_sudoku(self, event):
        self.basicsolve = Clock.schedule_interval(self.solve_step, 0.1)

    def solve_step(self, dt):
        # Erase any background colors left over
        self.clear_format()
        change = False
        change, errorcode = solve.basic_check(self.sudoku, change)

        # If there is an error, immedately assign the proper error
        if errorcode == 1:
            self.error_possible()
            self.basicsolve.cancel()
        elif errorcode == 2:
            self.error_double_assign()
            self.basicsolve.cancel()

        # If nothing changed, validate the answer
        if not change:
            solved, error = solve.validate_answer(self.sudoku)
            if solved:
                self.on_complete()
                self.basicsolve.cancel()
            elif error:
                self.textinput.text = 'ERROR Double Assignment'
            else:
                change, errorcode = solve.intermediate_check(
                    self.sudoku, change)
                if not change:
                    change, errorcode = solve.cross_check(self.sudoku, change)
                    change, errorcode = solve.intermediate_check(self.sudoku, change)
                    if not change:
                        self.error_unsolved()
                        self.basicsolve.cancel()

    def clear_format(self):
        color = [1, 1, 1, 1]
        for cell in self.cell_list:
            cell.color = color

    def on_complete(self):
        for cell in self.cell_list:
            cell.color = [0, 1, 0, 1]
        self.textinput.text = 'SOLVED'

    def error_unsolved(self):
        for cell in self.cell_list:
            cell.color = [1, 0, 0, 1]
        self.textinput.text = 'ERROR Unable To Complete Puzzle'

    def error_possible(self):
        self.textinput.text = 'ERROR No Possible Solutions Left for Cell'

    def error_double_assign(self):
        self.textinput.text = 'ERROR Double Assignment'

    def test(self, event):
        pass

    def change_entry(self, button):
        for but in button.parent.children:
            but.background_color = [1, 1, 1, 1]

        self.entry = int(button.text)
        button.background_color = [0, 1, 0, 1]

    def change_entry_type(self, button):

        button.background_color = [0, 1, 0, 1]
        # Check which button is being press
        if button.text == 'Pen':
            self.pen = True
            self.pencil = False
            # Clear color formatting on pencil button
            button.parent.children[0].background_color = [1, 1, 1, 1]

        else:
            self.pencil = True
            self.pen = False
            # Clear color formatting on pen button
            button.parent.children[1].background_color = [1, 1, 1, 1]

    def manual_entry(self, cell):
        if self.entry != '':
            if self.pen:
                # Assign the solution to the backend sudoku puzzle, not just the GUI element
                cell.cell.assign_solution(int(self.entry))
                cell.color = [1, 1, 1, 1]
            elif self.pencil:
                # Unlike with the pen, the pencil modifies a possible list that is only on the GUI element. It does not touch the backend
                if self.entry in cell.man_possible:
                    cell.man_possible.remove(int(self.entry))

                else:
                    cell.man_possible.add(int(self.entry))

                cell.update_possible(cell.man_possible)


sudoku = puzzle.build_sudoku(
    "200000001003060008807031940002506070409800056100000380038670500705090263000004000")

blank = puzzle.build_sudoku(
    "000000000000000000000000000000000000000000000000000000000000000000000000000000000")

if __name__ == '__main__':
    SudokuPy(blank).run()
