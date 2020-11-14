import puzzle_gui
import solve_gui

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

def testing(gui):
    print(gui.button_list[-2].text)


class SudokuPy(App):

    def __init__(self, sudoku, **kwargs):
        super(SudokuPy, self).__init__(**kwargs)
        self.sudoku = sudoku

    def build(self):

        root_widget = BoxLayout(orientation = 'vertical')

        puzzle = GridLayout(cols = 9, size_hint_y = 10)
        for rownum in range(9):
            for box in sudoku.loc[rownum]:
                puzzle.add_widget(Button(text= str(box.value)))

        print(self.sudoku)
        
        self.button_list = puzzle.children

        root_widget.add_widget(TextInput(text= 'Sudoku', size_hint_y = 1))
        root_widget.add_widget(puzzle)
        root_widget.add_widget(Button(text = 'Solve', on_release = self.solve_sudoku))

        return root_widget
    
    def solve_sudoku(self, event):
        _change = False
        _change = solve_gui.basic_check(self, self.sudoku, _change)
        print(sudoku)

    def test(self, event):
        testing(self)

sudoku = puzzle_gui.build_sudoku(
    "040100050107003960520008000000000017000906800803050620090060543600080700250097100")

if __name__ == '__main__':
    SudokuPy(sudoku).run()

