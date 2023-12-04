# /usr/bin/python3
# type: ignore
"""Day 20."""

import cv2
import numpy as np

KERNEL = 2**(np.reshape(np.array(list(range(8, -1, -1)), dtype=np.float32), (3, 3)))


class Img:
    def __init__(self, img: np.ndarray, algo: np.ndarray):
        self.img = cv2.copyMakeBorder(img, 15, 15, 15, 15, cv2.BORDER_CONSTANT, 0)
        self.algo = algo
        self.alternate: bool = (algo[0] == 1)
        self.background: int = 0

    def update(self):
        input = cv2.copyMakeBorder(self.img.astype(np.float32), 2, 2, 2, 2, borderType=cv2.BORDER_CONSTANT,
                                   value=self.background)
        output = cv2.filter2D(input, -1, KERNEL, borderType=cv2.BORDER_REPLICATE)[1:-1, 1:-1]
        self.img = self.algo[output.astype(int)]

        if self.alternate:
            self.background = 1 - self.background

    def count(self):
        return np.sum(self.img)

    def __repr__(self):
        viz = "\n".join(["".join([str(el) for el in row]).replace('0', '.').replace('1', '#') for row in self.img])
        return viz + "\n\n"


def _read_lines(path):
    with open(path) as f:
        all_rows = [row.strip().replace('.', '0').replace('#', '1') for row in f.readlines()]
        algo = np.array(list(all_rows[0]), dtype=int)

        img = np.array([list(row) for row in all_rows[2:]], dtype=int)

        return Img(img, algo)


def part_one(path: str) -> int:
    img = _read_lines(path)
    for _ in range(2):
        img.update()
    return img.count()


def part_two(path: str) -> int:
    img = _read_lines(path)
    for _ in range(50):
        img.update()
    return img.count()
