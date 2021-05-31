"""Toolbar.
"""

import tkinter as tk
from typing import Union


class Toolbar:
    """Left toolbar class.
    """
    TOOLBAR_WIDTH = 50
    COLOR_BG = '#3C3C3C'
    COLOR_SELECT = '#A0D500'

    def __init__(self, master: Union[tk.Widget, tk.Tk], height: int):
        """Init.
        """
        toolbar_frame = tk.Frame(master, width=self.TOOLBAR_WIDTH)
        toolbar_frame.pack(side=tk.LEFT)

        self._canvas = tk.Canvas(
            toolbar_frame,
            bg=self.COLOR_BG,
            width=self.TOOLBAR_WIDTH,
            height=height,
            highlightthickness=0
        )

        self._canvas.bind("<Button-1>", self._select)
        self._canvas.pack(expand=tk.Y, fill=tk.BOTH)

    def _select(self, event: tk.Event):
        """TODO: implement
        """
        print('Button pressed. To be implemented later.')
