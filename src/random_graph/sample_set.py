"""A special class that that can add, remove, and sample a random element efficiently.

Thanks to Stack Overflow user Amber for the scaffolding to create this class.
"""

import collections
import random
import typing

from . import utils


class SampleSet(object):
    def __init__(self, items: typing.Optional[typing.Iterable[collections.abc.Hashable]] = None) -> None:
        """This class allows for efficient addition, removal, and sampling of individual elements.

        This is achieved by maintaining a dictionary and a list simultaneously: the list has efficient sampling,
        while the dictionary has efficient addition and removal. Note that this class does not preserve order when
        adding or removing items.

        Args:
            items: the items to initialise the object with.

        Raises:
            ValueError: If there is a duplicate in the provided items.
        """
        if items is None:
            items = []
        if not utils.all_unique(items):
            raise ValueError("Duplicate items detected.")

        self.items = list(items)
        self.positions = {item: position for position, item in enumerate(self.items)}

    def replace(self, old: collections.abc.Hashable, new: collections.abc.Hashable, check: bool = True) -> None:
        """Replace the element at the given index with a new element.

        Args:
            old: the element to be removed.
            new: the element to be added.
            check: If True (the default), will check whether the new element is already present.

        Raises:
            ValueError: if the new element is already present.
        """
        if check and new in self.positions:
            raise ValueError("Item already present")
        position = self.positions.pop(old)
        self.positions[new] = position
        self.items[position] = new

    def add(self, item):
        if item in self.positions:
            raise ValueError("Item already present")
        self.items.append(item)
        self.positions[item] = len(self.items) - 1

    def remove(self, item):
        position = self.positions.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.positions[last_item] = position

    def choice(self):
        return random.choice(self.items)

    def __contains__(self, item):
        return item in self.positions

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]
