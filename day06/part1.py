import argparse
from typing import List


def find_marker(s: str) -> int:
    prev_chars: List[str] = []
    for i, e in enumerate(s):
        if len(prev_chars) < 4:
            prev_chars.append(e)
            continue
        prev_chars.append(e)
        prev_chars = prev_chars[1:]
        if len(set(prev_chars)) == 4:
            return i + 1
    raise ValueError("no unique set of 4 consecutive characters in string")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    print("case 0 (should be 7):", find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb"))
    print("case 1 (should be 5):", find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz"))
    print("case 2 (should be 6):", find_marker("nppdvjthqldpwncqszvftbrmjlhg"))
    print()
    with open(args.filename) as f:
        for line in f:
            print("from file:", find_marker(line))
