from __future__ import annotations

import argparse
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class File:
    name: str
    size: int

    @property
    def is_dir(self) -> bool:
        return False

    def pretty(self) -> str:
        return f"{self.name} (file, size={self.size})"


@dataclass
class Directory:
    name: str
    children: List[Union[Directory, File]] = field(default_factory=list)
    parent: Optional[Directory] = None

    @property
    def size(self) -> int:
        return sum(c.size for c in self.children)

    def _pretty(self) -> List[str]:
        out: List[str] = []
        out.append(f"- {self.name} (dir)")
        for c in self.children:
            if isinstance(c, File):
                out.append(f"\t- {c.pretty()}")
            else:
                assert isinstance(c, Directory)
                child_lines = [f"\t{l}" for l in c._pretty()]
                out += child_lines
        return out

    def pretty(self) -> str:
        return "\n".join(self._pretty())

    def list_all_children(self) -> List[Directory]:
        """List all children.

        This can count the same directory multiple times.
        Ex. if this dir has a child 'X' that contains 'Y' and 'Z',
        then this list will contain X *and* Y *and* Z.
        """
        children = [e for e in self.children if isinstance(e, Directory)]
        for child in [e for e in self.children if isinstance(e, Directory)]:
            children += child.list_all_children()
        return children


@dataclass
class Command:
    name: str
    output: List[str]


def parse_file(filename: str) -> List[Command]:
    """Parse cmd file, returning commands and their output."""
    commands: List[Command] = []

    with open(filename) as f:
        cmd = f.readline().strip()
        cmd_output: List[str] = []
        for line in f:
            if "$" in line:
                commands.append(Command(cmd, cmd_output))
                cmd = line.strip()
                cmd_output = []
            else:
                cmd_output.append(line.strip())
        commands.append(Command(cmd, cmd_output))
    return commands


_dir_re = re.compile(r"dir (\w+)")
_file_re = re.compile(r"(\d+) (.+)")


def do_commands(commands: List[Command]) -> Directory:
    """Run commands and return the root directory."""
    root = Directory(name="/")
    current_dir = root
    for command in commands:
        cmd = command.name

        # CD-type commands
        if cmd.startswith("$ cd"):
            if cmd.startswith("$ cd .."):
                assert current_dir.parent is not None
                current_dir = current_dir.parent
            elif cmd.startswith("$ cd /"):
                current_dir = root
            else:
                change_to = cmd.split()[-1]
                changed = False
                for child in current_dir.children:
                    if child.name == change_to:
                        assert isinstance(child, Directory)
                        changed = True
                        current_dir = child
                if not changed:
                    raise RuntimeError(
                        f"Cannot find child {change_to} in children of directory"
                        f" {current_dir}"
                    )

        # ls
        elif cmd.startswith("$ ls"):
            for line in command.output:
                if m := _dir_re.search(line):
                    new_dir = Directory(name=m.group(1), parent=current_dir)
                    current_dir.children.append(new_dir)
                elif m := _file_re.search(line):
                    new_file = File(name=m.group(2), size=int(m.group(1)))
                    current_dir.children.append(new_file)
                else:
                    raise RuntimeError(
                        f"Not sure what to do with ls output line `{line}`"
                    )

        else:
            raise RuntimeError(f"Not sure what to do with this command: {command}")

    return root


def do_part_1(root_dir: Directory) -> int:
    all_dirs = root_dir.list_all_children()
    return sum(d.size for d in all_dirs if d.size <= 100000)


def do_part_2(root_dir: Directory) -> int:
    total_space = 70000000
    need_space = 30000000

    current_free_space = total_space - root_dir.size

    best_dir = root_dir
    for d in root_dir.list_all_children():
        if current_free_space + d.size >= need_space:
            if d.size < best_dir.size:
                best_dir = d

    return best_dir.size


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="read a file")
    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()
    cmds = parse_file(args.filename)
    root = do_commands(cmds)
    print(do_part_1(root))
    print(do_part_2(root))
