"""see problem statement."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Elf:
    """One elf's work assignment."""

    start: int
    end: int

    def contains(self, other: Elf) -> bool:
        """Whether this elf's assignment fully contains the other elf's."""
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: Elf) -> bool:
        """Whether this elf's assignment overlaps the other elf's."""
        # It's actually easier for me to think about how to tell they don't overlap
        if self.start < other.start and self.end < other.start:
            return False
        if self.start > other.end and self.end > other.end:
            return False
        return True


@dataclass(frozen=True)
class Pair:
    """A pair of elves and their assignments."""

    elf1: Elf
    elf2: Elf

    def reconsider(self) -> bool:
        """Whether to reconsider this assignment.

        We reconsider an assignment if one elf's assignment
        *fully contains* the other.
        """
        return self.elf1.contains(self.elf2) or self.elf2.contains(self.elf1)

    def overlaps(self) -> bool:
        """Whether these two elves overlap."""
        return self.elf1.overlaps(self.elf2)


def count_reconsiders(filename: str) -> int:
    """How many pairs in this file need reconsidering."""
    assignment_re = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    count = 0
    with open(filename) as f:
        for line in f:
            m = assignment_re.search(line)
            if m is None:
                raise ValueError(
                    f"Not able to make pair from {line} in file {filename}"
                )
            p = Pair(
                Elf(int(m.group(1)), int(m.group(2))),
                Elf(int(m.group(3)), int(m.group(4))),
            )
            if p.reconsider():
                count += 1
    return count


def count_overlaps(filename: str) -> int:
    """How many pairs in this file overlaps."""
    assignment_re = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    count = 0
    with open(filename) as f:
        for line in f:
            m = assignment_re.search(line)
            if m is None:
                raise ValueError(
                    f"Not able to make pair from {line} in file {filename}"
                )
            p = Pair(
                Elf(int(m.group(1)), int(m.group(2))),
                Elf(int(m.group(3)), int(m.group(4))),
            )
            if p.overlaps():
                count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    print(count_reconsiders(args.filename))
    print(count_overlaps(args.filename))
