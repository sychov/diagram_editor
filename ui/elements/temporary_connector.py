"""Temporary connector realization.
"""

import tkinter as tk
from typing import Optional

from core.aliases import BezierCoords
from core.interfaces import Connector, Connectible, Removable


class TemporaryConnector(Connector, Removable):
    """Temporary connector realization.
    Directed arrow, from target to somewhere.
    """
    LINE_WIDTH = 4
    COLOR_TARGET_NOT_FOUND = '#A44'
    COLOR_TARGET_FOUND = '#6D6'

    def __init__(self, canvas: tk.Canvas, source: Connectible):
        """Init.
        """
        self._id = 'temporary-connector'
        self._canvas = canvas
        self._source = source
        self._target: Optional[Connectible] = None

        connector_tags = (self._id, )

        x, y = source.get_output_point()

        self._line = canvas.create_line(
            *self._get_bezier_coords(x, y, x, y),
            fill=self.COLOR_TARGET_NOT_FOUND,
            width=self.LINE_WIDTH,
            splinesteps=64,
            tags=connector_tags,
            arrow=tk.LAST,
            arrowshape=(12, 15, 5),
            smooth=True,
        )

    @staticmethod
    def _get_bezier_coords(x1: int, y1: int, x2: int, y2: int) -> BezierCoords:
        """Get coords of Bezier curve (4 points) in flatten tuple.
        Args: coords of the starting (x1, y1) and ending (x2, y2) point.
        """
        delta_x = x2 - x1
        delta_y = y2 - y1

        delta_x1 = max(abs(delta_x) // 3, 20)
        delta_y1 = max(delta_y // 10, 10)

        return (
            x1, y1,
            x1 + delta_x1, y1 + delta_y1,
            x2 - delta_x // 10,  y2 - delta_y // 10,
            x2, y2
        )

    def mark_as_target_is_found(self):
        """Remove selection focus from the node.
        """
        self._canvas.itemconfigure(
            self._line,
            fill=self.COLOR_TARGET_FOUND,
        )

    def mark_as_target_is_not_found(self):
        """Remove selection focus from the node.
        """
        self._canvas.itemconfigure(
            self._line,
            fill=self.COLOR_TARGET_NOT_FOUND,
        )

    def __repr__(self):
        """Simple representation.
        """
        return f'<Temporary connector line ID="{self._id}">'

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
        Doesn't need to temporary existed one.
        """
        pass

    # ---------------------- REMOVABLE ------------------------- #

    def delete(self):
        """Delete edge from canvas and registry.
        """
        self._canvas.delete(self._id)
