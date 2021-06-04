"""Enums.
"""

from dataclasses import dataclass
from enum import Enum


@dataclass
class Color:
    """Wrapper for gamma's color schema.
    """
    main_color: str
    secondary_color: str


# Enum for gamma set.
Gamma = Enum(
    'Gamma',
    {
        'BLUE': Color('#007BA0', '#1AAAD8'),
        'GREEN': Color('#7BA000', '#A0D500'),
        'RED': Color('#B2452E', '#D87765'),
        'VIOLET': Color('#5945B2', '#8477D1'),
        'YELLOW': Color('#919100', '#D6D61A'),
        'PURPLE': Color('#8600B2', '#C182D6'),
        'GRAY': Color('#6E9191', '#A1D6D6'),
    }.items()
)


class Type:
    """Workspace object's type.
    """
    NODE = 'node'
    LINE = 'line'


class Ability:
    """Workspace canvas item's ability.
    """
    DRAG = 'draggable'
    SELECT = 'selectable'


class TkEvents:
    """Used Tk events.
    """
    KEY_PRESSED = '<KeyPress>'
    MOUSE_LEFT_BUTTON_CLICK = '<Button-1>'
    MOUSE_LEFT_BUTTON_DOWN = '<ButtonPress-1>'
    MOUSE_LEFT_BUTTON_RELEASE = '<ButtonRelease-1>'
    MOUSE_LEFT_BUTTON_DRAG = '<B1-Motion>'
    MOUSE_RIGHT_BUTTON_DOWN = '<ButtonPress-3>'
    MOUSE_RIGHT_BUTTON_DRAG = '<B3-Motion>'


