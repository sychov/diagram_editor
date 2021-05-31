"""Diagram main workspace.
"""

import tkinter as tk
from typing import Union, Optional

from core.aliases import Coords, Tags
from core.enums import Gamma, Ability
from core.interfaces import Draggable, Selectable
from core.registry import RegistryMixin

from ui.elements.node import Node
from ui.elements.directed_edge import DirectedEdge


class Workspace:
    """Diagram workspace class.
    A place of Nodes and Connectors operations.
    """
    CANVAS_WIDTH = 3617
    CANVAS_HEIGHT = 2401
    EMPTY_FIELD_WIDTH = 50

    COLOR_BG = '#3C3C3C'
    COLOR_GRID = '#505050'
    COLOR_SELECT = '#A0D500'

    def __init__(self, master: Union[tk.Widget, tk.Tk]):
        """Init.
        """
        self._dragged_item: Optional[Draggable] = None
        self._selected_item: Optional[Selectable] = None
        self._last_coords: Coords

        # 1. Create workspace:

        workspace_frame = tk.Frame(master)
        workspace_frame.pack(side=tk.LEFT)

        self._canvas = tk.Canvas(
            workspace_frame,
            bg=self.COLOR_BG,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            confine=True,
            scrollregion=(
                -self.EMPTY_FIELD_WIDTH,
                -self.EMPTY_FIELD_WIDTH,
                self.CANVAS_WIDTH + self.EMPTY_FIELD_WIDTH,
                self.CANVAS_HEIGHT + self.EMPTY_FIELD_WIDTH
            )
        )
        self._canvas.pack(expand=tk.Y, fill=tk.BOTH)

        # 2. Draw workspaces grid:

        for y in range(0, self.CANVAS_HEIGHT, 32):
            self._canvas.create_line(
                0, y, self.CANVAS_WIDTH, y, fill=self.COLOR_GRID
            )
        for x in range(0, self.CANVAS_WIDTH, 32):
            self._canvas.create_line(
                x, 0, x, self.CANVAS_HEIGHT, fill=self.COLOR_GRID
            )

        # 3. Bind events:

        self._canvas.bind(
            "<ButtonPress-3>",
            lambda e: self._canvas.scan_mark(e.x, e.y)
        )
        self._canvas.bind(
            "<B3-Motion>",
            lambda e: self._canvas.scan_dragto(e.x, e.y, gain=1)
        )
        self._canvas.bind(
            "<ButtonPress-1>",
            self._callback_mouse_1_down
        )
        self._canvas.bind(
            "<B1-Motion>",
            self._callback_mouse_move
        )
        self._canvas.bind(
            "<ButtonRelease-1>",
            lambda e: setattr(self, '_dragged_item', None)
        )

    @staticmethod
    def _get_tag_id(tags: Tags) -> Optional[str]:
        """Get TagId from tags, if it exists.
        Return None, if not found.
        """
        for tag in tags:
            if tag.startswith('id-'):
                return tag
        else:
            return None

    def _get_absolute_coords(self, x: int, y: int) -> Coords:
        """Get absolute Canvas coords.
        This method should be used to transfer event's coords (taken from
        screen frame) to canvas coords.
        """
        x = self._canvas.canvasx(x)
        y = self._canvas.canvasy(y)
        return x, y

    def _callback_mouse_1_down(self, event: tk.Event):
        """Callback. Mouse button-1 was down.
        """
        x, y = self._get_absolute_coords(event.x, event.y)
        id_ = self._canvas.find_closest(x, y, halo=3)
        tags = self._canvas.gettags(id_)

        if self._selected_item:
            self._selected_item.clear_selection()
            self._selected_item = None

        if Ability.SELECT not in tags:
            return

        tag_id = self._get_tag_id(tags)
        item = RegistryMixin.get(tag_id)
        item.draw_selection()
        self._selected_item = item

        if Ability.DRAG not in tags:
            return

        self._dragged_item = item
        self._last_coords = x, y

    def _callback_mouse_move(self, event: tk.Event):
        """Callback. Mouse was moved.
        """
        if self._dragged_item:
            x, y = self._get_absolute_coords(event.x, event.y)
            x0, y0 = self._last_coords
            self._dragged_item.move(x - x0, y - y0)
            self._last_coords = x, y

    def test(self):
        """TODO: remove later.
        Just for test.
        """
        n1 = Node(self._canvas, 100, 100, Gamma.BLUE)
        n2 = Node(self._canvas, 500, 500, Gamma.GREEN)
        conn1 = DirectedEdge(self._canvas, n1, n2)

        n3 = Node(self._canvas, 200, 200, Gamma.YELLOW)
        n4 = Node(self._canvas, 400, 400, Gamma.RED)
        conn2 = DirectedEdge(self._canvas, n3, n4)

        conn3 = DirectedEdge(self._canvas, n2, n4)

        n5 = Node(self._canvas, 400, 400, Gamma.PURPLE)
        conn2 = DirectedEdge(self._canvas, n3, n5)
