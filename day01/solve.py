"""See the problem statement."""

import argparse
from string import digits
from typing import List


def read_elves(filename: str) -> List[int]:
    elves: List[int] = []

    current_elf = 0
    with open(filename, encoding="utf-8") as f:
        for line in f:
            if any(e in line for e in digits):
                current_elf += int(line)
            else:
                elves.append(current_elf)
                current_elf = 0
    return elves


def max_elf(elves: List[int]) -> int:
    return max(elves)


def top_three_elves(elves: List[int]) -> int:
    elves = elves.copy()
    top_three_sum = 0
    for _ in range(3):
        m = max(elves)
        elves.remove(m)
        top_three_sum += m
    return top_three_sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    elves = read_elves(args.filename)
    print(max_elf(elves))
    print(top_three_elves(elves))
