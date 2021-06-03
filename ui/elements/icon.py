"""Toolbar's icon.
"""

import tkinter as tk

from core.enums import Gamma, Ability, Type
from core.interfaces import Selectable
from core.registry import Registry


class Icon(Selectable):
    """Toolbar's icon class.
    """
    BORDER_WIDTH = 2

    def __init__(self, canvas: tk.Canvas, x: int, y: int, width: int,
                 height: int, gamma: Gamma):
        """Init.
        """
        self.gamma = gamma

        self._canvas = canvas
        self._id = Registry.add(self)
        node_tags = (Ability.SELECT, self._id)

        self._main_rect = canvas.create_rectangle(
            x,
            y,
            x + width,
            y + height,
            width=self.BORDER_WIDTH,
            outline='black',
            fill=gamma.value.main_color,
            tags=node_tags
        )
        self._inner_rect = canvas.create_rectangle(
            x + self.BORDER_WIDTH,
            y + self.BORDER_WIDTH + height // 3,
            x + width - self.BORDER_WIDTH,
            y + height - self.BORDER_WIDTH,
            width=0,
            fill=gamma.value.secondary_color,
            tags=node_tags
        )

    def __repr__(self):
        """Repr.
        """
        return f'<Icon ID="{self._id}">'

    # ---------------------- SELECTABLE ------------------------- #

    def draw_selection(self):
        """Put selection focus to the node.
        """
        self._canvas.itemconfigure(
            self._main_rect,
            outline='white',
            width=3,
            dash=(30,)
        )
        self._canvas.tag_raise(self._id)

    def clear_selection(self):
        """Remove selection focus from the node.
        """
        self._canvas.itemconfigure(
            self._main_rect,
            outline='black',
            width=2,
            dash=()
        )
