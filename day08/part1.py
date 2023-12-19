from __future__ import annotations

import argparse
from dataclasses import dataclass
from string import digits
from typing import Iterable, List


@dataclass
class Tree:
    height: int
    visible: bool = False

    def pretty(self) -> str:
        if self.visible:
            return f"{self.height}✔️"
        else:
            return f"{self.height}."


def trees_from_file(filename: str) -> List[List[Tree]]:
    """Read trees from an input file."""
    trees: List[List[Tree]] = []
    with open(filename) as f:
        for line in f:
            if line.strip() == "":
                continue
            tree_line = [Tree(int(c)) for c in line if c in digits]
            trees.append(tree_line)
    return trees


def _do_row(itree: Iterable[Tree]) -> None:
    """Mark row as visible, in the order determined by the iterator."""
    tallest_yet = -1
    for tree in itree:
        if tree.height > tallest_yet:
            tallest_yet = tree.height
            tree.visible = True


def mark_visible_rows(trees: List[List[Tree]]) -> None:
    for row in trees:
        _do_row(row)
        _do_row(reversed(row))


def mark_visible_columns(trees: List[List[Tree]]) -> None:
    count_cols = len(trees[0])
    count_rows = len(trees)

    for col in range(count_cols):
        tallest_yet = -1
        for row in range(count_rows):
            tree = trees[row][col]
            if tree.height > tallest_yet:
                tree.visible = True
                tallest_yet = tree.height

    for col in range(count_cols):
        tallest_yet = -1
        for row in reversed(range(count_rows)):
            tree = trees[row][col]
            if tree.height > tallest_yet:
                tree.visible = True
                tallest_yet = tree.height


def count_visible_trees(trees: List[List[Tree]]) -> int:
    mark_visible_rows(trees)
    mark_visible_columns(trees)

    count = 0
    for row in trees:
        for t in row:
            if t.visible:
                count += 1
    return count


def pretty_print_trees(trees: List[List[Tree]]):
    for row in trees:
        for t in row:
            print(f" {t.pretty()} ", end="")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    trees = trees_from_file(args.filename)
    print(count_visible_trees(trees))
    pretty_print_trees(trees)
