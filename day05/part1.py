from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from itertools import islice
from string import ascii_lowercase, ascii_uppercase
from typing import List, Tuple

_op_str_re = re.compile(r"move (\d+) from (\d+) to (\d+)")

# Recipe from python itertools page. thanks python itertools page
def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


# end recipe


@dataclass(frozen=True)
class Op:
    """One operation."""

    how_many: int
    where_from: int
    where_to: int

    @classmethod
    def from_str(cls, s: str):
        """Create from a string like 'move 3 from 2 to 1'."""
        m = _op_str_re.search(s)
        if m is None:
            raise ValueError(f"string {s} is not in the right format")
        return cls(
            how_many=int(m.group(1)),
            where_from=int(m.group(2)),
            where_to=int(m.group(3)),
        )


@dataclass
class Crane:
    stacks: List[List[str]]

    def do(self, op: Op):
        # zero-indexing vs one-indexing
        where_from = op.where_from - 1
        where_to = op.where_to - 1
        for _ in range(op.how_many):
            crate = self.stacks[where_from].pop()
            self.stacks[where_to].append(crate)

    def pretty(self) -> str:
        longest_stack = max(len(s) for s in self.stacks)
        copy_stacks: List[List[str]] = []
        for stack in self.stacks:
            copy = [f"[{e}] " for e in stack.copy()]
            while len(copy) < longest_stack:
                copy.append("    ")
            copy.reverse()
            copy_stacks.append(copy)
        out = ""
        for row in range(longest_stack):
            for stack in copy_stacks:
                out += stack[row]
            out += "\n"
        for i in range(1, len(copy_stacks) + 1):
            out += f" {i}  "
        out += "\n"
        return out

    def top_of_each_stack(self) -> List[str]:
        """What's on top of each stack?"""
        return [stack[-1] for stack in self.stacks if len(stack) != 0]

    def message(self) -> str:
        """Make a 'message' from the crane on top of each stack."""
        out = ""
        for c in self.top_of_each_stack():
            out += c
        return out


def crane_from_file(filename: str) -> Crane:
    """Read crane from file."""
    # Python doesn't have do/while so I'm going to use my secret knowledge
    # that i got from reading the input file:
    # there are 9 stacks
    stacks: List[List[str]] = []
    for _ in range(0, 9):
        stacks.append([])

    with open(filename) as f:
        for line in f:
            if line.strip() == "":
                break
            # Let's be real: we could look for those square braces
            # or we could just split the crane platform into groups of 4 characters.
            for i, batch in enumerate(batched(line, 4)):
                for char in batch:
                    if char in ascii_uppercase:
                        stacks[i].append(char)
    for stack in stacks:
        stack.reverse()
    return Crane(stacks)


def ops_from_file(filename: str) -> List[Op]:
    """Read operations from file."""
    with open(filename) as f:
        # Skip down until we get to the blank line
        line = f.readline()
        while line.strip() != "":
            line = f.readline()
        # Here is where the ops start
        return [Op.from_str(line) for line in f]


def do_file(filename: str) -> str:
    """Make a crane, operate the whole file, get the message."""
    crane = crane_from_file(filename)
    ops = ops_from_file(filename)
    for o in ops:
        crane.do(o)
    return crane.message()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    print(do_file(args.filename))
