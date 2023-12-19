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
    start: Cell = Cell(0, 0)
    knots: List[Cell] = field(default_factory=list)

    tail_visited: DefaultDict[int, DefaultDict[int, bool]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(bool))
    )

    @classmethod
    def len10(cls, start=Cell(0, 0)) -> Rope:
        """Make a new rope with a head and 9 "tail" knots."""
        knots: List[Cell] = []
        for _ in range(0, 10):
            knots.append(Cell(start.x, start.y))
        return cls(start=start, knots=knots)

    def __post_init__(self):
        self.tail_visited[self.start.x][self.start.y] = True

    def move_head(self, direction: str):
        head = self.knots[0]
        if direction == LEFT:
            head.y -= 1
        elif direction == RIGHT:
            head.y += 1
        elif direction == UP:
            head.x -= 1
        elif direction == DOWN:
            head.x += 1
        else:
            raise ValueError(f"Not sure what kinda direction {direction} is")

        self._catch_up_tail()
        tail = self.knots[-1]
        self.tail_visited[tail.x][tail.y] = True
        # print("Moved tail", self.head, self.tail)
        # print(self.print_travel())

    def _catch_up_tail(self):
        for i, head in enumerate(self.knots[:-1]):
            tail = self.knots[i + 1]
            if head.within_one(tail):
                continue

            if head.x == tail.x:
                if head.y > tail.y:
                    tail.y += 1
                else:
                    tail.y -= 1
            elif head.y == tail.y:
                if head.x > tail.x:
                    tail.x += 1
                else:
                    tail.x -= 1

            else:
                # We are moving diagonally
                if head.x < tail.x:
                    tail.x -= 1
                else:
                    tail.x += 1
                if head.y < tail.y:
                    tail.y -= 1
                else:
                    tail.y += 1

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
        for knot in self.knots:
            if knot.x < min_x:
                min_x = knot.x
            if knot.x > max_x:
                max_x = knot.x
            if knot.y < min_y:
                min_y = knot.y
            if knot.y > max_y:
                max_y = knot.y
        out = ""
        # print(min_x, max_x, min_y, max_y)
        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                if self.knots[0].x == i and self.knots[0].y == j:
                    out += "H"
                    continue
                has_knot = False
                for knot_index in range(1, len(self.knots)):
                    if self.knots[knot_index].x == i and self.knots[knot_index].y == j:
                        out += str(knot_index)
                        has_knot = True
                        break
                if has_knot:
                    continue
                elif self.tail_visited[i][j]:
                    out += "#"
                else:
                    out += "."
            out += "\n"
        return out.rstrip()


def do_thing(filename: str) -> Rope:
    rope = Rope.len10()
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
