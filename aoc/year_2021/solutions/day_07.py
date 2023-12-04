# /usr/bin/python3
"""Day 7."""

import numpy as np


def _read_lines(path):
    with open(path) as f:
        row = f.readlines()[0].strip().split(',')
        return np.array(row, dtype=int)


# def part_one(path)->int:
#     values = np.sort(_read_lines(path))
#     n = len(values)

#     scores = []
#     score = np.sum(values-values[0])
#     last_val = values[0]
#     for idx, val in enumerate(values):
#         score += (val - last_val)*(idx - (n-idx))
#         scores.append(score)
#         last_val = val

#     # Assume the answer is a number that was in the input (since the burning cost is constant)
#     best_id = np.argmin(scores)
#     print(f"{scores[best_id]} fuel at x={values[best_id]}")


def part_one(path: str) -> int:
    values = _read_lines(path)

    def get_score(val):
        diff = np.abs(values-val)
        return int(np.sum(diff))  # L1 distance

    scores = [get_score(val) for val in values]

    best_id = np.argmin(scores)
    print(f"{scores[best_id]} fuel at x={values[best_id]}")
    return scores[best_id]


def part_two(path: str) -> int:
    values = np.sort(_read_lines(path))

    def get_score(val):
        diff = np.abs(values-val)
        return int(np.sum(0.5*diff*(diff+1)))  # n(n+1)/2

    scores = [get_score(val) for val in values]
    # plt.plot(values, scores)
    # plt.show()

    best_indices = np.argsort(scores)
    best_val_min = np.min(values[best_indices[:2]])
    best_val_max = np.max(values[best_indices[:2]])

    refinement_scores = [get_score(best_val_min+k) for k in range(best_val_max-best_val_min+1)]
    best_diff = np.argmin(refinement_scores)
    print(f"{refinement_scores[best_diff]} fuel at x={best_val_min +best_diff}")

    return refinement_scores[best_diff]
