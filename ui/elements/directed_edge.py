"""Base Connector realization, DirectedEdge.
"""

import tkinter as tk

from core.aliases import BezierCoords
from core.interfaces import Connector, Connectible, Selectable, Removable
from core.enums import Ability
from core.registry import Registry


class DirectedEdge(Connector, Selectable, Removable):
    """Base Connector realization.
    Directed arrow, from target to source.
    """
    LINE_WIDTH = 3
    COLOR = '#AAA'

    def __init__(self, canvas: tk.Canvas, source: Connectible,
                 target: Connectible):
        """Init.
        """
        self._id = Registry.add(self)
        self._canvas = canvas
        self._source = source
        self._target = target

        connector_tags = (Ability.SELECT, self._id)

        x1, y1 = source.get_output_point()
        x2, y2 = target.get_input_point()

        self._line = canvas.create_line(
            *self._get_bezier_coords(x1, y1, x2, y2),
            fill=self.COLOR,
            width=self.LINE_WIDTH,
            splinesteps=64,
            tags=connector_tags,
            arrow=tk.LAST,
            arrowshape=(12, 15, 5),
            smooth=True,
        )

        source.add_output_connector(self)
        target.add_input_connector(self)

    @staticmethod
    def _get_bezier_coords(x1: int, y1: int, x2: int, y2: int) -> BezierCoords:
        """Get coords of Bezier curve (4 points) in flatten tuple.
        Args: coords of the starting (x1, y1) and ending (x2, y2) point.
        """
        delta_x = max(abs(x2 - x1) // 3, 30)
        delta_y = max((y2 - y1) // 10, 10)
        return (
            x1, y1,
            x1 + delta_x, y1 + delta_y,
            x2 - delta_x - 20, y2 - delta_y,
            x2, y2
        )

    def __repr__(self):
        """Simple representation.
        """
        return f'<Connector line ID="{self._id}">'

    # ---------------------- CONNECTOR ------------------------- #

    @property
    def source(self):
        """Source of connector.
        """
        return self._source

    def move_target_point(self, delta_x: int, delta_y: int):
        """Move connector's target point.
        """
        x1, y1, *_, x2, y2 = self._canvas.coords(self._id)
        x2 += delta_x
        y2 += delta_y
        self._canvas.coords(self._id, *self._get_bezier_coords(x1, y1, x2, y2))

    def move_source_point(self, delta_x: int, delta_y: int):
        """Move connector's source point.
        """
        x1, y1, *_, x2, y2 = self._canvas.coords(self._id)
        x1 += delta_x
        y1 += delta_y
        self._canvas.coords(self._id, *self._get_bezier_coords(x1, y1, x2, y2))

    # ---------------------- SELECTABLE ------------------------- #

    def draw_selection(self):
        """Put selection focus to the node.
        """
        self._canvas.itemconfigure(
            self._line,
            fill='cyan',
            dash=(6, 4)
        )
        self._canvas.tag_raise(self._id)

    def clear_selection(self):
        """Remove selection focus from the node.
        """
        self._canvas.itemconfigure(
            self._line,
            fill=self.COLOR,
            dash=()
        )

    # ---------------------- REMOVABLE ------------------------- #

    def delete(self):
        """Delete edge from canvas and registry.
        """
        self._source.remove_output_connector(self)
        self._target.remove_input_connector(self)
        self._canvas.delete(self._id)
        Registry.delete(self._id)
