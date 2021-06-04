"""Registry mixin.
"""

from typing import Any, Optional
from collections import defaultdict

from core.aliases import Tags


class Registry:
    """Registry to adding items by special tag_id, based on their class
    and amount of items of this class.
    """
    REGISTRY = {}
    COUNTERS = defaultdict(int)

    @classmethod
    def add(cls, item: Any) -> str:
        """Add item to registry.
        Return item's tag_id.
        """
        category = item.__class__
        cls.COUNTERS[category] += 1
        name = f'id-{category.__name__.lower()}-{cls.COUNTERS[category]}'
        cls.REGISTRY[name] = item
        return name

    @classmethod
    def get(cls, tag_id: str) -> Any:
        """Get item from registry by name.
        """
        return cls.REGISTRY[tag_id]

    @classmethod
    def delete(cls, tag_id: str) -> Any:
        """Get item from registry by name.
        """
        del cls.REGISTRY[tag_id]

    @staticmethod
    def get_id_from_tags(tags: Tags) -> Optional[str]:
        """Get TagId from tags, if it exists.
        Return None, if not found.
        """
        for tag in tags:
            if tag.startswith('id-'):
                return tag
        else:
            return None