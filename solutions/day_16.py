# /usr/bin/python3
"""Day 16."""

from typing import List, Optional, Set, Tuple
import numpy as np
from dataclasses import dataclass

hexa_to_bin_dict = {'0': "0000",
                    '1': "0001",
                    '2': "0010",
                    '3': "0011",
                    '4': "0100",
                    '5': "0101",
                    '6': "0110",
                    '7': "0111",
                    '8': "1000",
                    '9': "1001",
                    'A': "1010",
                    'B': "1011",
                    'C': "1100",
                    'D': "1101",
                    'E': "1110",
                    'F': "1111"}


def bin_list_to_decimal(bin_list):
    return sum(int(v) << i for i, v in enumerate(bin_list[::-1]))


@dataclass
class Info:
    start_idx: int = 0
    version: int = -1


def get_next_packet(bin_code: np.ndarray, start_idx: int) -> Optional[Info]:
    try:
        version = bin_list_to_decimal(bin_code[start_idx:start_idx+3])
        start_idx += 3
        type_id = bin_list_to_decimal(bin_code[start_idx:start_idx+3])
        start_idx += 3

        if type_id == 4:  # Literal value
            blocks = []
            while True:
                first_bit = bin_code[start_idx]
                start_idx += 1
                blocks.append(bin_code[start_idx:start_idx+4])
                start_idx += 4
                if first_bit == 0:
                    break
            val = bin_list_to_decimal(np.concatenate(blocks))
        else:
            length_type_id = bin_code[start_idx]
            start_idx += 1
            if length_type_id == 0:
                total_bit_length = bin_list_to_decimal(bin_code[start_idx:start_idx+15])
                start_idx += 15
            else:
                nb_sub_packets = bin_list_to_decimal(bin_code[start_idx:start_idx+11])
                start_idx += 11
        return Info(start_idx=start_idx, version=version)
    except IndexError:
        return None


def _read_lines(path):
    with open(path) as f:
        row = f.readlines()[0].strip()
        for k, v in hexa_to_bin_dict.items():
            row = row.replace(k, v)
        return np.array(list(row), dtype=int)


def part_one(path: str) -> int:
    bin_code = _read_lines(path)

    sum_versions = 0
    info: Optional[Info] = Info(start_idx=0)
    while True:
        info = get_next_packet(bin_code, info.start_idx)
        if info is None:
            break
        sum_versions += info.version

    return sum_versions


def part_two(path: str) -> int:
    #
    #
    #
    #
    #
    #
    #     TODO
    #
    #
    #
    #
    #
    #
    #
    return 0
