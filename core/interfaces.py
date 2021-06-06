"""Set of app interfaces.
"""

from abc import ABC, abstractmethod

from core.aliases import Coords


class Draggable(ABC):
    """Workspace item, that can be dragged.
    """
    @abstractmethod
    def move(self, delta_x: int, delta_y: int):
        """Move item within workspace.
        """
        pass


class Selectable(ABC):
    """Workspace item, that can be selected.
    """
    @abstractmethod
    def draw_selection(self):
        """Put selection focus to the item.
        """
        pass

    @abstractmethod
    def clear_selection(self):
        """Remove selection focus from the item.
        """
        pass


class Connector(ABC):
    """Workspace item, that can connect Connectible items.
    """
    @property
    @abstractmethod
    def source(self) -> 'Connectible':
        """
        """
        pass

    @abstractmethod
    def move_target_point(self, delta_x: int, delta_y: int):
        """Move connector's target point.
        """
        pass

    @abstractmethod
    def move_source_point(self, delta_x: int, delta_y: int):
        """Move connector's source point.
        """
        pass


class Targetable(ABC):
    """Workspace item, that can be targeted with the temporary connector.
    """
    @abstractmethod
    def turn_highlight_on(self):
        """Put highlight to the item.
        """
        pass

    @abstractmethod
    def turn_highlight_off(self):
        """Remove highlight to the item.
        """
        pass

    @abstractmethod
    def is_already_connected_with(self, source: 'Connectible'):
        """Check, if the item is already connected with the source.
        """
        pass


class Connectible(Targetable):
    """Workspace item, that can be connected with others trough Connector.
    Also, can be target for temporary connector.
    """
    @abstractmethod
    def add_input_connector(self, connector: Connector):
        """Add connector for input.
        """
        pass

    @abstractmethod
    def add_output_connector(self, connector: Connector):
        """Add connector for output.
        """
        pass

    @abstractmethod
    def remove_input_connector(self, connector: Connector):
        """Remove connector for input.
        """
        pass

    @abstractmethod
    def remove_output_connector(self, connector: Connector):
        """Remove connector for output.
        """
        pass

    @abstractmethod
    def get_output_point(self) -> Coords:
        """Get starting point coords for connector.
        """
        pass

    @abstractmethod
    def get_input_point(self) -> Coords:
        """Get ending point coords for connector.
        """
        pass


class Removable(ABC):
    """Workspace item, that can be deleted.
    """
    @abstractmethod
    def delete(self):
        """Remove item.
        """
        pass
