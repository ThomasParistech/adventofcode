# /usr/bin/python3
"""Day 6."""


def _read_lines(path: str) -> str:
    with open(path) as f:
        return f.read().strip()


def _find_pattern(line: str, size: int) -> int:
    n_chars = len(line)
    for k in range(size-1, n_chars):
        crt_set = set(line[k+1-size:k+1])
        if len(crt_set) == size:
            return k+1
    return -1


def part_one(path: str) -> int:
    line = _read_lines(path)
    return _find_pattern(line, 4)


def part_two(path: str) -> int:
    line = _read_lines(path)
    return _find_pattern(line, 14)
