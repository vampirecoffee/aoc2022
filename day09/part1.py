from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, List

LEFT = "L"
RIGHT = "R"
UP = "U"
DOWN = "D"


@dataclass
class Cell:
    x: int
    y: int

    def within_one(self, other: Cell) -> bool:
        if abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1:
            return True
        else:
            return False


@dataclass
class Rope:
    head: Cell = Cell(0, 0)
    tail: Cell = Cell(0, 0)

    tail_visited: DefaultDict[int, DefaultDict[int, bool]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(bool))
    )

    def __post_init__(self):
        self.tail_visited[self.tail.x][self.tail.y] = True

    def move_head(self, direction: str):
        # print("Current position:", self.head, self.tail)
        # print("Moving in direction", direction)
        if direction == LEFT:
            self.head.y -= 1
        elif direction == RIGHT:
            self.head.y += 1
        elif direction == UP:
            self.head.x -= 1
        elif direction == DOWN:
            self.head.x += 1
        else:
            raise ValueError(f"Not sure what kinda direction {direction} is")

        if self.head.within_one(self.tail):
            # print("Don't have to move tail", self.head, self.tail)
            # print(self.print_travel())
            return

        if self.head.x == self.tail.x:
            if self.head.y > self.tail.y:
                self.tail.y += 1
            else:
                self.tail.y -= 1
        elif self.head.y == self.tail.y:
            if self.head.x > self.tail.x:
                self.tail.x += 1
            else:
                self.tail.x -= 1

        else:
            # We are moving diagonally
            if self.head.x < self.tail.x:
                self.tail.x -= 1
            else:
                self.tail.x += 1
            if self.head.y < self.tail.y:
                self.tail.y -= 1
            else:
                self.tail.y += 1

        self.tail_visited[self.tail.x][self.tail.y] = True
        # print("Moved tail", self.head, self.tail)
        # print(self.print_travel())

    def total_visited(self) -> int:
        """Return total number of cells that tail visited."""
        total = 0
        for row in self.tail_visited.values():
            total += sum(1 for cell in row.values() if cell)
        return total

    def print_travel(self) -> str:
        """Print cells visited by tail."""
        min_x = 10000
        max_x = -10000
        min_y = 10000
        max_y = -10000
        for i, row in self.tail_visited.items():
            if any(visited for visited in row.values()):
                if i > max_x:
                    max_x = i
                if i < min_x:
                    min_x = i
                for j, visited in row.items():
                    if visited:
                        if j > max_y:
                            max_y = j
                        if j < min_y:
                            min_y = j
        if self.head.x < min_x:
            min_x = self.head.x
        if self.head.x > max_x:
            max_x = self.head.x
        if self.head.y < min_y:
            min_y = self.head.y
        if self.head.y > max_y:
            max_y = self.head.y
        out = ""
        # print(min_x, max_x, min_y, max_y)
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                if self.head.x == i and self.head.y == j:
                    out += "H"
                elif self.tail.x == i and self.tail.y == j:
                    out += "T"
                elif self.tail_visited[i][j]:
                    out += "#"
                else:
                    out += "."
            out += "\n"
        return out.rstrip()


def do_thing(filename: str) -> Rope:
    rope = Rope()
    with open(filename) as f:
        for line in f:
            # print()
            # print(line.strip())
            direction, steps_str = line.split()
            steps = int(steps_str)
            for _ in range(steps):
                rope.move_head(direction)
    return rope


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    rope = do_thing(args.filename)
    print(rope.total_visited())
    # print(rope.print_travel())
