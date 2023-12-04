# /usr/bin/python3
# type: ignore
"""Day 13."""

import numpy as np


def hash_array(x: np.ndarray) -> str:
    return "".join([str(val) for val in x.flatten()])


letters_dict = {hash_array(np.array([[0, 0, 1, 1, 0],
                                     [0, 0, 0, 1, 0],
                                     [0, 0, 0, 1, 0],
                                     [0, 0, 0, 1, 0],
                                     [1, 0, 0, 1, 0],
                                     [0, 1, 1, 0, 0]])): "J",
                hash_array(np.array([[0, 1, 1, 0, 0],
                                     [1, 0, 0, 1, 0],
                                     [1, 0, 0, 0, 0],
                                     [1, 0, 0, 0, 0],
                                     [1, 0, 0, 1, 0],
                                     [0, 1, 1, 0, 0]])): "C",
                hash_array(np.array([[1, 1, 1, 0, 0],
                                     [1, 0, 0, 1, 0],
                                     [1, 0, 0, 1, 0],
                                     [1, 1, 1, 0, 0],
                                     [1, 0, 1, 0, 0],
                                     [1, 0, 0, 1, 0]])): "R",
                hash_array(np.array([[1, 0, 0, 1, 0],
                                     [1, 0, 0, 1, 0],
                                     [1, 1, 1, 1, 0],
                                     [1, 0, 0, 1, 0],
                                     [1, 0, 0, 1, 0],
                                     [1, 0, 0, 1, 0]])): "H",
                hash_array(np.array([[1, 1, 1, 1, 0],
                                     [1, 0, 0, 0, 0],
                                     [1, 1, 1, 0, 0],
                                     [1, 0, 0, 0, 0],
                                     [1, 0, 0, 0, 0],
                                     [1, 1, 1, 1, 0]])): "E",
                hash_array(np.array([[1, 1, 1, 1, 1],
                                     [1, 0, 0, 0, 1],
                                     [1, 0, 0, 0, 1],
                                     [1, 0, 0, 0, 1],
                                     [1, 1, 1, 1, 1],
                                     [0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0]])): "O"
                }


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        split_idx = all_rows.index("\n")

        # Dots
        dots = np.array([all_rows[k].strip().split(",") for k in range(split_idx)], dtype=int)
        x_max = np.max(dots[:, 0])
        y_max = np.max(dots[:, 1])
        mask_dots = np.zeros((y_max+1, x_max+1), dtype=bool)
        for xy in dots:
            mask_dots[xy[1], xy[0]] = True

        # Fold instructions
        instructions = [all_rows[k].strip().split("fold along ")[-1].split("=")
                        for k in range(split_idx+1, len(all_rows))]
        instructions = [(direction == "x", int(val)) for direction, val in instructions]

        return mask_dots, instructions


def part_one(path: str) -> int:
    mask_dots, instructions = _read_lines(path)

    is_x, val = instructions[0]
    if is_x:
        folded_dots = np.flip(mask_dots[:, val+1:], axis=1)
        mask_dots = mask_dots[:, :val] | folded_dots
    else:
        folded_dots = np.flip(mask_dots[val+1:, :], axis=0)
        mask_dots = mask_dots[:val, :] | folded_dots

    return np.sum(mask_dots)


def part_two(path: str) -> int:
    mask_dots, instructions = _read_lines(path)

    for is_x, val in instructions:
        if is_x:
            folded_dots = np.flip(mask_dots[:, val+1:], axis=1)
            mask_dots = mask_dots[:, :val] | folded_dots
        else:
            folded_dots = np.flip(mask_dots[val+1:, :], axis=0)
            mask_dots = mask_dots[:val, :] | folded_dots

    digit_width = 5
    n_digits = mask_dots.shape[1]//digit_width

    letters = []
    for k in range(n_digits):
        letter = mask_dots[:, k*digit_width:(k+1)*digit_width].astype(int)
        letters.append(letters_dict[hash_array(letter)])

    answer = "".join(letters)
    print(f"Answer is a string and not an int: {answer}")
    return len(answer)
