"""Toolbar.
"""

import tkinter as tk
from typing import Union, Optional

from core.enums import Gamma, Ability, TkEvents
from core.registry import Registry

from ui.elements.icon import Icon


class Toolbar:
    """Left toolbar class.
    """
    TOOLBAR_WIDTH = 60
    TOOLBAR_HEIGHT = 2000
    COLOR_BG = '#303030'
    COLOR_SELECT = '#A0D500'

    def __init__(self, master: Union[tk.Widget, tk.Tk]):
        """Init.
        """
        self._selected_item: Optional[Icon] = None

        toolbar_frame = tk.Frame(master, width=self.TOOLBAR_WIDTH)
        toolbar_frame.pack(side=tk.LEFT)

        self._canvas = tk.Canvas(
            toolbar_frame,
            bg=self.COLOR_BG,
            width=self.TOOLBAR_WIDTH,
            height=self.TOOLBAR_HEIGHT,
            highlightthickness=0
        )

        self._canvas.bind(
            TkEvents.MOUSE_LEFT_BUTTON_CLICK,
            self._callback_mouse_1
        )
        self._canvas.pack(expand=tk.Y, fill=tk.BOTH)

        # --------------- JUST FOR TESESING ---------------- #

        for n, gamma in enumerate(Gamma):
            Icon(
                canvas=self._canvas,
                x=5,
                y=35 * n + 5,
                width=self.TOOLBAR_WIDTH - 10,
                height=30,
                gamma=gamma
            )

    def _callback_mouse_1(self, event: tk.Event):
        """Callback. Mouse button-1 was pressed.
        """
        id_ = self._canvas.find_closest(event.x, event.y, halo=0)
        tags = self._canvas.gettags(id_)
        last_selected = self.pop_selected()

        if Ability.SELECT in tags:
            tag_id = Registry.get_id_from_tags(tags)
            item = Registry.get(tag_id)

            if item != last_selected:
                item.draw_selection()
                self._selected_item = item

    def pop_selected(self) -> Optional[Icon]:
        """Get Icon instance and clear selection, if selected.
        None instead.
        """
        item = self._selected_item
        if item:
            self._drop_selection()
            return item

    def _drop_selection(self):
        """Remove selection focus from Icon.
        """
        if self._selected_item:
            self._selected_item.clear_selection()
            self._selected_item = None
