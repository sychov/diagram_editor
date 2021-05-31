"""Typing aliases.
"""

# Coordinates pair: x, y:
Coords = tuple[int, int]

# 4 pairs of points Coordinates in tuple: x1, y1, x2, y2, x3, y3, x4, y4:
BezierCoords = tuple[int, int, int, int, int, int, int, int]

# Tags - sequence of strings, got from Tk Canvas object:
Tags = tuple[str]
