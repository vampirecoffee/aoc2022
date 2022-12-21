"""See problem statement."""

import argparse
from dataclasses import dataclass, field
from itertools import islice
from string import ascii_lowercase, ascii_uppercase
from typing import List, Set


def priority(item: str) -> int:
    """Get priority of an item."""
    if len(item) != 1:
        raise ValueError("Item should be exactly one character")
    if item in ascii_lowercase:
        # values are 1 through 26
        return ascii_lowercase.index(item) + 1
    elif item in ascii_uppercase:
        # values are 27 through 52
        return ascii_uppercase.index(item) + 27
    else:
        raise ValueError(f"{item} is not a letter")


@dataclass(frozen=True)
class Group:
    """A group of 3 elves, each with their own rucksack.

    We don't actually care about the front and back of these rucksacks,
    so they're just strings.
    """

    sack1: str
    sack2: str
    sack3: str

    def badge(self) -> str:
        """Get badge for this group.

        A group's badge is the item shared between all 3 sacks.
        """
        for item in self.sack1:
            if item in self.sack2 and item in self.sack3:
                return item
        raise RuntimeError("This group has no badge :(")

    def priority(self) -> int:
        """Get priority for this group."""
        return priority(self.badge())


def batch3(iterable):
    """Return batches of 3.

    From the Iterables recipe.
    """
    it = iter(iterable)
    while batch := tuple(islice(it, 3)):
        yield batch


def groups_from_file(filename: str) -> List[Group]:
    groups: List[Group] = []
    with open(filename) as f:
        for sack1, sack2, sack3 in batch3(f):
            groups.append(Group(sack1, sack2, sack3))
    return groups


def prioritize_groups(groups: List[Group]) -> int:
    """Get the sum of the priorities of the groups."""
    return sum(g.priority() for g in groups)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    groups = groups_from_file(args.filename)
    print(prioritize_groups(groups))
