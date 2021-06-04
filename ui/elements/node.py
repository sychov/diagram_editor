"""Workspace's node.
"""

import tkinter as tk

from core.aliases import Coords
from core.enums import Gamma, Ability, Type
from core.interfaces import Draggable, Connectible, Selectable, Connector, \
    Removable
from core.registry import Registry


class Node(Draggable, Connectible, Selectable, Removable):
    """Workspaces node class.
    """
    BORDER_WIDTH = 2
    CONNECTION_AREA_RADIUS = 12

    def __init__(self, canvas: tk.Canvas, x: int, y: int, gamma: Gamma):
        """Init.
        """
        # TODO: change to dynamic values later
        width = 200
        height = 100
        header_height = 32

        self._canvas = canvas
        self._gamma = gamma
        self._id = Registry.add(self)

        # TODO: change later
        self._text_head = 'Hello'
        self._text_desc = 'My name is Alex\nWhat is your name?'

        self._input_connectors = []
        self._output_connectors = []

        self._node_tags = (Ability.DRAG, Ability.SELECT, Type.NODE, self._id)

        self._main_rect = canvas.create_rectangle(
            x,
            y,
            x + width,
            y + height,
            width=self.BORDER_WIDTH,
            outline='black',
            fill=gamma.value.main_color,
            tags=self._node_tags
        )
        self._inner_rect = canvas.create_rectangle(
            x + self.BORDER_WIDTH,
            y + self.BORDER_WIDTH + header_height,
            x + width - self.BORDER_WIDTH,
            y + height - self.BORDER_WIDTH,
            width=0,
            fill=gamma.value.secondary_color,
            tags=self._node_tags,
        )
        self._head_text = canvas.create_text(
            x + width // 2,
            y + header_height // 2,
            fill='white',
            text=self._text_head,
            font=('Verdana', '12'),
            tags=self._node_tags,
        )
        self._inner_text = canvas.create_text(
            x + width // 2,
            y + (height + header_height) // 2,
            fill='black',
            text=self._text_desc,
            font=('Verdana', '12'),
            tags=self._node_tags,
        )
        self._output_point_area = None

    def __repr__(self):
        """Repr.
        """
        return f'<Node ID="{self._id}">'

    # ---------------------- CONNECTIBLE ------------------------- #

    def get_output_point(self) -> Coords:
        """Get connector's starting point.
        """
        x1, y1, x2, y2 = self._canvas.coords(self._inner_rect)
        return x2 + 2, (y1 + y2) // 2

    def get_input_point(self) -> Coords:
        """Get connector's ending point.
        """
        x1, y1, x2, y2 = self._canvas.coords(self._inner_rect)
        return x1 - 2, (y1 + y2) // 2

    def add_input_connector(self, connector: Connector):
        """Add connector for input.
        """
        self._input_connectors.append(connector)

    def add_output_connector(self, connector: Connector):
        """Add connector for output.
        """
        self._output_connectors.append(connector)

    def remove_input_connector(self, connector: Connector):
        """Remove connector for input.
        """
        self._input_connectors.remove(connector)

    def remove_output_connector(self, connector: Connector):
        """Remove connector for output.
        """
        self._output_connectors.remove(connector)

    # ---------------------- DRAGGABLE -------------------------- #

    def move(self, delta_x: int, delta_y: int):
        """Move node in workspace.
        """
        self._canvas.move(self._id, delta_x, delta_y)
        for connector in self._input_connectors:
            connector.move_target_point(delta_x, delta_y)
        for connector in self._output_connectors:
            connector.move_source_point(delta_x, delta_y)

    # ---------------------- SELECTABLE ------------------------- #

    def draw_selection(self):
        """Put selection focus to the node.
        """
        self._canvas.itemconfigure(
            self._main_rect,
            outline='cyan',
            width=3,
            dash=(30,)
        )

        center_x, center_y = self.get_output_point()

        self._output_point_area = self._canvas.create_oval(
            center_x - self.CONNECTION_AREA_RADIUS,
            center_y - self.CONNECTION_AREA_RADIUS,
            center_x + self.CONNECTION_AREA_RADIUS,
            center_y + self.CONNECTION_AREA_RADIUS,
            width=3,
            fill=self._gamma.value.secondary_color,
            outline=self._gamma.value.main_color,
            tags=self._node_tags
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
        self._canvas.delete(self._output_point_area)
        self._output_point_area = None

    # ---------------------- REMOVABLE ------------------------- #

    def delete(self):
        """Delete edge from canvas and registry.
        """
        for q in self._input_connectors + self._output_connectors:
            q.delete()
        self._canvas.delete(self._id)
        Registry.delete(self._id)
