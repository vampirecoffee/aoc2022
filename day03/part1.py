"""See problem statement."""

import argparse
from dataclasses import dataclass, field
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
class Rucksack:
    # Let's just call the two compartments the "front" and "back"
    front: str
    back: str

    def __post_init__(self):
        if len(self.front) != len(self.back):
            raise ValueError(
                "Front and back compartments must contain the same number of items"
            )

    @classmethod
    def from_sack(cls, sack: str):
        if len(sack) % 2 != 0:
            raise ValueError(
                "Rucksack must contain the same number of items in its front and back"
                " compartments"
            )
        half_len = int(len(sack) / 2)
        return cls(sack[:half_len], sack[half_len:])

    def shared_item(self) -> List[str]:
        """Get the item(s) that are in both compartments."""
        shared: Set[str] = set()
        for item in self.front:
            if item in self.back:
                shared.add(item)
        return list(shared)

    def priority(self) -> int:
        """Get the priority of this rucksack.

        A priority is the sum of the priorities of the items that are shared
        between both compartments.
        """
        return sum(priority(e) for e in self.shared_item())


def sacks_from_file(filename: str) -> List[Rucksack]:
    sacks: List[Rucksack] = []
    with open(filename) as f:
        for line in f:
            sacks.append(Rucksack.from_sack(line.strip()))
    return sacks


def prioritize_sacks(sacks: List[Rucksack]) -> int:
    """Get the sum of the priorities of all 'shared' items across rucksacks."""
    return sum(s.priority() for s in sacks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    sacks = sacks_from_file(args.filename)
    print(prioritize_sacks(sacks))
