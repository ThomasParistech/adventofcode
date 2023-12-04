# /usr/bin/python3
"""Day 3."""

import copy

import numpy as np
import pandas as pd


def bin_list_to_decimal(bin_list):
    return sum(int(v) << i for i, v in enumerate(bin_list[::-1]))


def part_one(path: str) -> int:
    with open(path) as f:
        all_rows = f.readlines()
        n_rows = len(all_rows)
        bit_counts = np.zeros(len(all_rows[0].strip()))
        for row in all_rows:
            row = row.strip()
            for idx, c in enumerate(row):
                if c == '1':
                    bit_counts[idx] += 1

    gamma_rate = bit_counts >= n_rows/2
    event_rate = bit_counts < n_rows/2

    gamma_rate_val = bin_list_to_decimal(gamma_rate)
    event_rate_val = bin_list_to_decimal(event_rate)

    # print("".join([str(int(b)) for b in gamma_rate]))
    # print("".join([str(int(b)) for b in event_rate]))
    return gamma_rate_val*event_rate_val


def part_two(path: str) -> int:
    data = pd.read_csv(path, header=None, names=["bin"], dtype=str)
    input_list_bits = np.array([np.array(list(b), dtype=int).astype(bool)
                               for b in data["bin"]])

    def get_rate(list_bits, most):
        idx = 0
        while len(list_bits) > 1:
            common_1_bits = list_bits[:, idx]
            num_1_bits = np.sum(common_1_bits)
            if most:
                select = num_1_bits >= len(list_bits)/2
            else:
                select = num_1_bits < len(list_bits)/2

            if select:
                list_bits = list_bits[common_1_bits]
            else:
                list_bits = list_bits[np.logical_not(common_1_bits)]
            idx += 1
        assert len(list_bits) == 1
        return bin_list_to_decimal(list_bits[0])

    oxygen_rate = get_rate(copy.deepcopy(input_list_bits), True)
    co2_rate = get_rate(copy.deepcopy(input_list_bits), False)
    print(f"{oxygen_rate} {co2_rate} => {oxygen_rate*co2_rate}")
    return oxygen_rate*co2_rate
