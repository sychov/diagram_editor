"""Diagram main workspace.
"""

import tkinter as tk
from typing import Union, Optional, Callable

from core.aliases import Coords, TkEvent
from core.enums import Ability, TkEvents
from core.interfaces import Draggable, Selectable, Removable, Connectible
from core.registry import Registry

from ui.elements.node import Node
from ui.elements.icon import Icon
from ui.elements.directed_edge import DirectedEdge
from ui.elements.temporary_connector import TemporaryConnector


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
        self._temp_connector: Optional[TemporaryConnector] = None
        self._current_target: Optional[Connectible] = None
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
            self._callback_mouse_1_drag
        )
        self._canvas.bind(
            TkEvents.MOUSE_LEFT_BUTTON_RELEASE,
            self._callback_mouse_1_up
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

    def _callback_mouse_1_down(self, event: TkEvent):
        """Callback. Mouse button-1 was down.
        """
        self._canvas.focus_set()
        x, y = self._get_absolute_coords(event.x, event.y)
        self._last_coords = x, y

        # Check, if some icon on toolbar was previously selected.
        # Create a new element, if it was.
        toolbar_icon = self._pop_selection_from_toolbar()
        if toolbar_icon:
            Node(self._canvas, x - 10, y - 10, toolbar_icon.gamma)

        id_ = self._canvas.find_closest(x, y, halo=3)
        tags = self._canvas.gettags(id_)
        if self._selected_item:
            if Ability.CONNECT_SOURCE in tags:
                # Start temporary connector flow, instead of selection/drag.
                self._temp_connector = TemporaryConnector(
                    self._canvas,
                    self._selected_item
                )
                return

            self._selected_item.clear_selection()
            self._selected_item = None

        if Ability.SELECT in tags:
            tag_id = Registry.get_id_from_tags(tags)
            item = Registry.get(tag_id)
            item.draw_selection()
            self._selected_item = item

            if Ability.DRAG in tags:
                self._dragged_item = item

    def _callback_mouse_1_up(self, _: TkEvent):
        """Callback. Mouse button-1 was up.
        """
        # disable dragging mode
        self._dragged_item = None

        # that's all, if we have no active temporary connector...
        if not self._temp_connector:
            return

        # ...otherwise, let's create permanent connector, if we have a target.
        if self._current_target:
            self._current_target.turn_highlight_off()
            DirectedEdge(
                self._canvas,
                source=self._temp_connector.source,
                target=self._current_target
            )
            self._current_target = None
            self._canvas.tag_raise(
                Registry.get_tag_id(self._temp_connector.source)
            )

        # ...and delete temporary connector in any case.
        self._temp_connector.delete()
        self._temp_connector = None

    def _callback_mouse_1_drag(self, event: TkEvent):
        """Callback. Mouse was moved.
        """
        x, y = self._get_absolute_coords(event.x, event.y)
        if self._temp_connector:
            self._move_temporary_connector(x, y)
        elif self._dragged_item:
            self._drag_current(x, y)

    def _move_temporary_connector(self, x: int, y: int):
        """Move target point of temporary connector.
        """
        # 1. Move temporary connector:
        x0, y0 = self._last_coords
        self._temp_connector.move_target_point(x - x0, y - y0)
        self._last_coords = x, y

        # 2. Check for possible Connectible obj, target it, if we can:
        for id_ in self._canvas.find_overlapping(x, y, x + 1, y + 1):
            tags = self._canvas.gettags(id_)
            if Ability.CONNECT in tags:
                tag_id = Registry.get_id_from_tags(tags)
                item = Registry.get(tag_id)
                if self._try_to_target_item(item):
                    return

        # 3. Otherwise, clear
        if self._current_target:
            self._current_target.turn_highlight_off()
            self._current_target = None
            self._temp_connector.mark_as_target_is_not_found()

    def _try_to_target_item(self, item: Connectible) -> bool:
        """Try to target some Connectible by curent temporary connector.
        Returns True, if was success, else False.
        """
        # We don't need to target connector's source
        if item == self._temp_connector.source:
            return False

        # We don't need to re-target the same node:
        if item == self._current_target:
            return True

        # We don't want to target already connected node:
        if item.is_already_connected_with(self._temp_connector.source):
            return False

        # Otherwise, let's target this node:
        if self._current_target:
            self._current_target.turn_highlight_off()
        self._current_target = item
        item.turn_highlight_on()
        self._temp_connector.mark_as_target_is_found()
        return True

    def _drag_current(self, x: int, y: int):
        """Drag previously selected item.
        """
        x0, y0 = self._last_coords
        self._dragged_item.move(x - x0, y - y0)
        self._last_coords = x, y

    def _callback_key_pressed(self, event: TkEvent):
        """Callback. Pressed some key.
        """
        if event.keysym == 'Delete' and self._selected_item \
                and isinstance(self._selected_item, Removable):
            self._selected_item.delete()
            self._selected_item = None
