# /usr/bin/python3
"""Day 7."""

from typing import List, Optional, Dict
import numpy as np
from dataclasses import dataclass, field


@dataclass
class Directory:
    total_size: int = 0
    local_size: int = 0
    children: Dict[str, 'Directory'] = field(default_factory=dict)
    parent: Optional['Directory'] = None

    def update_total(self):
        self.total_size = self.local_size
        for child in self.children.values():
            child.update_total()
            self.total_size += child.total_size

    def list_subdir_sizes(self, sizes: List[int]):
        sizes.append(self.total_size)
        for child in self.children.values():
            child.list_subdir_sizes(sizes)


def _read_lines(path: str) -> Directory:
    with open(path) as f:
        root = Directory()
        crt_node = root
        rows = [row.strip() for row in f.readlines()]
        index = 0
        while index < len(rows):
            row = rows[index]
            index += 1
            if row == "$ cd /":
                crt_node = root
            elif row == "$ cd ..":
                assert crt_node.parent is not None
                crt_node = crt_node.parent
            elif row.startswith("$ cd "):
                dst = row.split(" ")[-1]
                if not dst in crt_node.children:
                    crt_node.children[dst] = Directory(parent=crt_node)
                crt_node = crt_node.children[dst]
            else:  # ls
                while index < len(rows) and not rows[index].startswith("$"):
                    begin = rows[index].split(" ")[0]
                    if begin != "dir":
                        crt_node.local_size += int(begin)
                    index += 1

        root.update_total()
        return root


def part_one(path: str) -> int:
    root = _read_lines(path)

    sizes = []
    root.list_subdir_sizes(sizes)
    sizes = np.array(sizes)
    return np.sum(sizes[sizes <= 100000])


def part_two(path: str) -> int:
    root = _read_lines(path)
    sizes = []
    root.list_subdir_sizes(sizes)

    space_needed = 30000000 - (70000000 - root.total_size)
    sizes = np.array(sizes)
    sizes = sizes[sizes >= space_needed]
    return np.min(sizes)
