from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from kivy.properties import (ListProperty, NumericProperty)
from kivy.uix.modalview import ModalView
from kivy.lang import Builder

class GridEntry(Button):
    coords = ListProperty([0, 0])

class TicTacToeGrid(GridLayout):
    status = ListProperty([0, 0, 0,
                           0, 0, 0,
                           0, 0, 0])
    current_player = NumericProperty(-1)

    def __init__(self, *args, **kwargs):
        super(TicTacToeGrid, self).__init__(*args, **kwargs)

        for row in range(3):
           for column in range(3):
               grid_entry = GridEntry(
                        coords=(row, column))
               grid_entry.bind(on_release=self.button_pressed)
               grid_entry.font_size = 200
               self.add_widget(grid_entry)

    def button_pressed(self, button):
        # Create player symbol and colour lookups
        player = {1: 'O', -1: 'X'}
        colours = {1: (1, 0, 0, 1), -1: (0, 1, 0, 1)} # (r, g, b, a)
        row, column = button.coords # The pressed button is automatically
                              # passed as an argument

        # Convert 2D grid coordinates to 1D status index
        status_index = 3*row + column
        already_played = self.status[status_index]

        # If nobody has played here yet, make a new move
        if not already_played:
            self.status[status_index] = self.current_player
            button.text = player[self.current_player]
            button.background_color = colours[self.current_player]
            self.current_player *= -1 # Switch current player
            self.BotRunning()

    def BotRunning(self, *args):
        for row in range(3):
            for column in range(3):
                status_index = 3 * row + column
                if self.status[status_index] == -1:
                    status_index1 = 3 * (row + 1) + column

    def reset(self, *args):
            self.status = [0 for _ in range(9)]

            for child in self.children:
                child.text = ''
                child.background_color = (1, 1, 1, 1)

            self.current_player = -1

    def on_status(self, instance, new_value):
        status = new_value

        # Sum each row, column and diagonal.
        # Could be shorter, but let's be extra
        # clear what’s going on

        sums = [sum(status[0:3]), # rows
               sum(status[3:6]), sum(status[6:9]), sum(status[0::3]), # columns
               sum(status[1::3]), sum(status[2::3]), sum(status[::4]), # diagonals
               sum(status[2:-2:2])]

        # Sums can only be +-3 if one player
        # filled the whole line
        winner = None

        if -3 in sums:
            winner = 'Крестик Выиграл!'
        elif 3 in sums:
            winner = 'Нолик Выиграл!'
        elif 0 not in self.status:
            winner = 'Ничья....!'

        if winner:
            popup = ModalView(size_hint=(0.75, 0.5))
            victory_label = Label(text=winner, font_size=50)
            popup.add_widget(victory_label)
            popup.bind(on_dismiss=self.reset)
            popup.open()

class Interface(BoxLayout):
        pass

Builder.load_string("""
<TicTacToeGrid>:
    cols: 3
<GridEntry>:
    font_size: self.height
<Interface>:
    orientation: 'vertical'
    # We add child widgets in kv by simply writing another
    # layer in the widget tree, nested as deep as we like

""")

class KrestikiNoliki(App):
    def build(self):
        return TicTacToeGrid()


if __name__ == '__main__':
    KrestikiNoliki().run()
