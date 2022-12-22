from __future__ import annotations

import argparse
from dataclasses import dataclass
from string import digits
from typing import Iterable, List, Tuple


@dataclass
class Tree:
    height: int
    visible: bool = False
    up: int = 0
    down: int = 0
    left: int = 0
    right: int = 0

    def pretty(self) -> str:
        if self.visible:
            return f"{self.height}✔️"
        else:
            return f"{self.height}."

    def score(self) -> int:
        return self.up * self.down * self.left * self.right


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


def score_trees(trees: List[List[Tree]]):
    for i, row in enumerate(trees):
        for j, tree in enumerate(row):
            # Up
            for up_i in range(i - 1, -1, -1):
                tree.up += 1
                if trees[up_i][j].height >= tree.height:
                    break

            # Down
            for down_i in range(i + 1, len(trees)):
                tree.down += 1
                if trees[down_i][j].height >= tree.height:
                    break

            # Left
            for left_j in range(j - 1, -1, -1):
                tree.left += 1
                if trees[i][left_j].height >= tree.height:
                    break

            # Right
            for right_j in range(j + 1, len(row)):
                tree.right += 1
                if trees[i][right_j].height >= tree.height:
                    break


def get_best_tree(trees: List[List[Tree]]) -> Tuple[Tree, Tuple[int, int]]:
    """Get the best-scoring tree in the list of trees."""
    best_tree = Tree(height=0)
    coordinates = (-1, -1)
    for i, row in enumerate(trees):
        for j, tree in enumerate(row):
            if tree.score() > best_tree.score():
                best_tree = tree
                coordinates = (i, j)

    return best_tree, coordinates


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
    score_trees(trees)
    best_tree, coordinates = get_best_tree(trees)
    print(
        "The best tree is",
        best_tree,
        "with a score of",
        best_tree.score(),
        "at coordinates",
        coordinates,
    )
