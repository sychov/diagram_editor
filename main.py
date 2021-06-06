"""Diagram editor.
Main application.
"""

import tkinter as tk

from ui.workspace import Workspace
from ui.toolbar import Toolbar


class Main:
    """Main application class.
    """
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800

    def __init__(self):
        """Init.
        """
        self._root = tk.Tk()
        self._root['bg'] = 'green'
        self._root.title('Diagram editor')
        self._root.geometry(
            f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+100+100'
        )

        self._toolbar = Toolbar(self._root)
        self._workspace = Workspace(
            self._root,
            pop_selection_from_toolbar_callback=self._toolbar.pop_selected
        )

    def run(self):
        """Run application.
        """
        self._root.mainloop()


# ---- START ---- #

if __name__ == '__main__':
    Main().run()
