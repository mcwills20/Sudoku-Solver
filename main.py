import puzzle
import solve
import solve_utils as utils
import backtrack

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior


class SudokuCell(ButtonBehavior, GridLayout):

    color = ListProperty([1, 1, 1, 1])

    def __init__(self, cell, **kwargs):
        super(SudokuCell, self).__init__(**kwargs)

        self.backend_cell = cell
        self.initialize()

    def initialize(self):

        if self.backend_cell.value == 0:

            self.possible = self.backend_cell.possible
            self.man_possible = set()
            for labelid in self.ids:
                self.ids[labelid].text = ''

        else:
            self.update_solution(self.backend_cell.value)
            # Turn the background color back to white
            self.color = [1, 1, 1, 1]
            self.ids.pos5.color = [1, 0, 1, 1]

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

    def backtrack_update(self, value):
        if value != 0:
            self.ids.pos5.text = str(value)
            self.ids.pos5.font_size = 25
            self.ids.pos5.color = [0, 0, 0, 1]
        else:
            self.ids.pos5.text = ''


class BoxGrid(GridLayout):
    def __init__(self, **kwargs):
        super(BoxGrid, self).__init__(**kwargs)


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
        for box in range(9):
            puzzle.add_widget(self.build_box(box))
        interface.add_widget(puzzle)

        # Add the manual buttons
        interface.add_widget(ManualInput())

        # Add manual puzzle entry window
        puzzleentry = BoxLayout(orientation='horizontal', size_hint=(1, .1))

        puzzleentry.add_widget(
            TextInput(text='Enter Puzzle as String Here', size_hint=(.7, 1)))
        puzzleentry.add_widget(
            Button(text='Build', on_release=self.build_entry, size_hint=(.3, 1)))

        # Build the app
        root_widget.add_widget(puzzleentry)
        root_widget.add_widget(interface)
        root_widget.add_widget(
            Button(text='Smart Solve', on_release=self.solve_sudoku, size_hint=(1, .05)))
        root_widget.add_widget(
            Button(text='Backtrack Solve', on_release=self.solve_backtrack, size_hint=(1, .05)))

        # Store a reference to the textinput for easy manipulation later
        self.textinput = root_widget.children[-1].children[-1]

        # Initialize a solved value
        self.solved = False

        return root_widget

    def build_box(self, boxnum):
        box = utils.get_box(boxnum, self.sudoku)

        grid = BoxGrid()

        for cell in utils.iter_box(box):
            cell.gui = SudokuCell(cell)
            grid.add_widget(cell.gui)
            self.cell_list.append(cell.gui)

        return grid

    # When solved button is press, create an event to cycle through the smart solve steps
    def solve_sudoku(self, event):
        
        if not self.solved:

            self.smartsolve = Clock.schedule_interval(self.solve_step, 0.1)
        
        else:
            self.textinput.text = 'This is already solved, why would you want to solve again?'

    def solve_step(self, dt):
        # Erase any background colors left over
        self.clear_format()
        change = False
        change, errorcode = solve.basic_check(self.sudoku, change)

        # If there is an error, immedately assign the proper error
        if errorcode == 1:
            self.error_possible()
            self.smartsolve.cancel()
        elif errorcode == 2:
            self.error_double_assign()
            self.smartsolve.cancel()

        # If nothing changed, validate the answer
        if not change:
            solved, error = solve.validate_answer(self.sudoku)
            if solved:
                self.on_complete()
                self.smartsolve.cancel()
            elif error:
                self.textinput.text = 'ERROR: Double Assignment'
                self.smartsolve.cancel()
            else:
                change, errorcode = solve.intermediate_check(
                    self.sudoku, change)
                if not change:
                    change, errorcode = solve.cross_check(self.sudoku, change)
                    change, errorcode = solve.intermediate_check(
                        self.sudoku, change)
                    if not change:
                        self.error_unsolved()
                        self.smartsolve.cancel()

    def on_complete(self):
        # Set color to Green
        self.iter_cells_color([0, 1, 0, 1])
        self.textinput.text = 'SOLVED'
        self.solved = True

    def error_unsolved(self):
        self.color_red()
        self.textinput.text = 'ERROR: Unable To Complete Puzzle, Try Backtrack'

    def error_possible(self):
        self.textinput.text = 'ERROR: No Possible Solutions Left for Cell'

    def error_double_assign(self):
        self.textinput.text = 'ERROR: Double Assignment'

    def solve_backtrack(self, event):
        
        if not self.solved:

            self.clear_format()
            self.clear_gui_possible()
            # Start the recursive function at the first cell, going forward
            self.backtrack_next = (0, 0)
            self.forward = True
            self.backtrack = Clock.schedule_interval(
                self.backtrack_step, 0.0000001)
        
        else:
            self.textinput.text = 'This is already solved, why would you want to solve again?'

    def backtrack_step(self, dt):
        # If the backtrack is going backwards on the first cell, there is no possible solution
        if self.backtrack_next == ('Beginning', 'Beginning'):
            self.color_red()
            self.textinput.text = 'ERROR: Backtrack Failed No Solution Possible'
            self.backtrack.cancel()
        # If the backtrack is complete, check to see if it is solved
        elif self.backtrack_next == ('End', 'End'):
            solved, _ = solve.validate_answer(self.sudoku)
            if solved:
                self.on_complete()
            else:
                self.textinput.text = 'ERROR: Backtrack Failed No Solution Possible'
                self.color_red()
            self.backtrack.cancel()
        else:
            self.backtrack_next, self.forward = backtrack.backtrack(
                self.sudoku, self.backtrack_next, self.forward)


    def manual_entry(self, cell):
        if self.entry != '':
            if self.pen:
                if not cell.backend_cell.original:
                    if cell.backend_cell.value == self.entry:
                        cell.backend_cell.reinit()
                    else:
                        # Assign the solution to the backend sudoku puzzle, not just the GUI element
                        cell.backend_cell.assign_solution(int(self.entry))
                        cell.color = [1, 1, 1, 1]
                else:
                    self.textinput.text = 'Cell is original, cannot be manually changed'


            elif self.pencil:
                if not cell.backend_cell.solved:
                    # Unlike with the pen, the pencil modifies a possible list that is only on the GUI element. It does not touch the backend
                    if self.entry in cell.man_possible:
                        cell.man_possible.remove(int(self.entry))

                    else:
                        cell.man_possible.add(int(self.entry))

                    cell.update_possible(cell.man_possible)
                else:
                    self.textinput.text = 'Cannot pencil in possible answers for a solved cell'

    def change_entry(self, button):
        for but in button.parent.children:
            # Reset all number pad buttons to default background
            but.background_color = [1, 1, 1, 1]

        self.entry = int(button.text)
        # Set color to green
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

    def build_entry(self, event):

        if len(self.textinput.text) == 81:

            entry = utils.entry_generator(self.textinput.text)

            for cell in utils.iter_box(self.sudoku):
                try:
                    _value = int(next(entry))
                except:
                    self.textinput.text = 'ERROR: Entry not numbers'
                    return None
                cell.reinit()
                if _value != 0:
                    cell.assign_solution(_value)
                    cell.gui.color = [1, 1, 1, 1]
                    cell.gui.ids.pos5.color = [0, 0, 0, 1]
                    cell.mutable = False
                    cell.original = True

            self.solved = False

        else:
            self.textinput.text = 'ERROR: Entry not 81 characters'

    def clear_format(self):
        self.iter_cells_color([1, 1, 1, 1])

    def color_red(self):
        self.iter_cells_color([1, 0, 0, 1])

    def iter_cells_color(self, color):
        for cell in self.cell_list:
            cell.color = color

    def clear_gui_possible(self):
        # Clear the possible pencil marks during backtracking
        for cell in self.cell_list:
            if cell.backend_cell.mutable:
                for child in cell.children:
                    child.text = ''


if __name__ == '__main__':

    blank = puzzle.build_sudoku(
        "000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    SudokuPy(blank).run()
