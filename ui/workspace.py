"""Diagram main workspace.
"""

import tkinter as tk
from typing import Union, Optional, Callable

from core.aliases import Coords
from core.enums import Gamma, Ability, TkEvents
from core.interfaces import Draggable, Selectable, Removable
from core.registry import Registry

from ui.elements.node import Node
from ui.elements.icon import Icon
from ui.elements.directed_edge import DirectedEdge


class Workspace:
    """Diagram workspace class.
    A place of Nodes and Connectors operations.
    """
    CANVAS_WIDTH = 3585
    CANVAS_HEIGHT = 2305
    EMPTY_FIELD_WIDTH = 50

    COLOR_BG = '#3C3C3C'
    COLOR_GRID = '#505050'
    COLOR_SELECT = '#A0D500'

    def __init__(self,
                 master: Union[tk.Widget, tk.Tk],
                 pop_selection_from_toolbar_callback: Callable[[], Icon]):
        """Init.
        """
        self._dragged_item: Optional[Draggable] = None
        self._selected_item: Optional[Selectable] = None
        self._last_coords: Coords

        self._pop_selection_from_toolbar = pop_selection_from_toolbar_callback

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

        for y in range(0, self.CANVAS_HEIGHT, 128):
            self._canvas.create_line(
                0, y, self.CANVAS_WIDTH, y, fill=self.COLOR_GRID
            )
        for x in range(0, self.CANVAS_WIDTH, 128):
            self._canvas.create_line(
                x, 0, x, self.CANVAS_HEIGHT, fill=self.COLOR_GRID
            )

        # 3. Bind events:

        self._canvas.bind(
            TkEvents.MOUSE_RIGHT_BUTTON_DOWN,
            lambda e: self._canvas.scan_mark(e.x, e.y)
        )
        self._canvas.bind(
            TkEvents.MOUSE_RIGHT_BUTTON_DRAG,
            lambda e: self._canvas.scan_dragto(e.x, e.y, gain=1)
        )
        self._canvas.bind(
            TkEvents.MOUSE_LEFT_BUTTON_DOWN,
            self._callback_mouse_1_down
        )
        self._canvas.bind(
            TkEvents.MOUSE_LEFT_BUTTON_DRAG,
            self._callback_mouse_move
        )
        self._canvas.bind(
            TkEvents.MOUSE_LEFT_BUTTON_RELEASE,
            lambda e: setattr(self, '_dragged_item', None)
        )
        self._canvas.bind(
            TkEvents.KEY_PRESSED,
            self._callback_key_pressed
        )

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
        self._canvas.focus_set()
        x, y = self._get_absolute_coords(event.x, event.y)

        toolbar_icon = self._pop_selection_from_toolbar()
        if toolbar_icon:
            Node(self._canvas, x - 10, y - 10, toolbar_icon.gamma)

        id_ = self._canvas.find_closest(x, y, halo=3)
        tags = self._canvas.gettags(id_)

        if self._selected_item:
            self._selected_item.clear_selection()
            self._selected_item = None

        if Ability.SELECT not in tags:
            return

        tag_id = Registry.get_id_from_tags(tags)
        item = Registry.get(tag_id)
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

    def _callback_key_pressed(self, event: tk.Event):
        """Callback. Pressed some key.
        """
        if event.keysym == 'Delete' and self._selected_item \
                and isinstance(self._selected_item, Removable):
            self._selected_item.delete()
            self._selected_item = None

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
