# /usr/bin/python3
"""Day 16."""

from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Tuple


@dataclass
class Valve:
    rate: int
    children: List[str] = field(default_factory=list)
    distances: Dict[str, int] = field(default_factory=dict)

    def compute_distances(self, self_name: str, valves: Dict[str, 'Valve']):
        djikstra_set: Dict[str, int] = {self_name: 0}
        unknown = list(valves.keys())

        while len(djikstra_set) != 0:
            valve_to_add = min(djikstra_set.keys(), key=(lambda k: djikstra_set[k]))
            dist = djikstra_set.pop(valve_to_add)
            unknown.remove(valve_to_add)
            if valves[valve_to_add].rate != 0 and valve_to_add != self_name:
                self.distances[valve_to_add] = dist

            for child in valves[valve_to_add].children:
                if child in unknown:
                    new_dist = dist + 1
                    if child in djikstra_set:
                        djikstra_set[child] = min(new_dist, djikstra_set[child])
                    else:
                        djikstra_set[child] = new_dist


def _read_lines(path: str) -> Dict[str, Valve]:
    with open(path) as f:

        valves: Dict[str, Valve] = {}
        for row in f.readlines():
            row = row.strip()
            for old, new in [("Valve ", ""), (" has flow rate=", "|"), ("; tunnels lead to valves ", "|"),
                             ("; tunnel leads to valve ", "|")]:
                row = row.replace(old, new)
            name, rate, children = row.split("|")
            valves[name] = Valve(rate=int(rate),
                                 children=children.split(", "))

        for name, valve in valves.items():
            if name == "AA" or valve.rate != 0:
                valve.compute_distances(name, valves)

        valves = {name: valve for name, valve in valves.items() if valve.rate != 0 or name == "AA"}

        return valves


MAXI_PRESSURE = -1
BEST_PATH = ""


def part_one(path: str) -> int:
    valves = _read_lines(path)

    def backtrack(path_names: List[str], pressure: int, time: int):
        global MAXI_PRESSURE
        global BEST_PATH
        if pressure > MAXI_PRESSURE:
            MAXI_PRESSURE = pressure
            BEST_PATH = "->".join(path_names)

        crt_valve = valves[path_names[-1]]
        for child, dist in crt_valve.distances.items():
            if child in path_names:
                continue

            next_time = time+dist+1
            if next_time > 30:
                continue

            backtrack(path_names+[child], pressure + valves[child].rate * (30-next_time), next_time)

    backtrack(["AA"], 0, 0)
    print(BEST_PATH, MAXI_PRESSURE)

    return MAXI_PRESSURE


def part_two(path: str) -> int:
    valves = _read_lines(path)
    assert len(valves) <= 16  # Bit manip

    names_to_index: Dict[str, int] = {name: k for k, name in enumerate(valves.keys())}
    rates: List[int] = [valve.rate for valve in valves.values()]
    distances: List[List[Tuple[int, int]]] = [[(names_to_index[child], dist)
                                               for child, dist in valve.distances.items()]
                                              for valve in valves.values()]  # idx and distance

    anagrams_score: Dict[int, int] = {}

    def backtrack(anagrams_score: Dict[int, int], path_indices: List[int], hash_idx: int, pressure: int, time: int):
        anagrams_score[hash_idx] = max(pressure, anagrams_score.get(hash_idx, 0))

        for child, dist in distances[path_indices[-1]]:
            if child in path_indices:
                continue

            next_time = time+dist+1
            if next_time > 26:
                continue

            backtrack(anagrams_score, path_indices+[child], hash_idx | (1 << child),
                      pressure + rates[child] * (26-next_time), next_time)

    backtrack(anagrams_score, [0], 0, 0, 0)

    list_anagrams_score: List[Tuple[int, int]] = list(anagrams_score.items())
    n_anagrams = len(list_anagrams_score)
    print(f"{n_anagrams} anagrams")

    max_pressure = 0
    for i, (set_i, p_i) in enumerate(list_anagrams_score):
        for set_j, p_j in list_anagrams_score[:i]:
            if set_i & set_j == 0:
                max_pressure = max(max_pressure, p_i+p_j)

    return max_pressure
