# /usr/bin/python3
"""Day 16."""


from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass, field


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

        return valves


MAXI_PRESSURE = -1
BEST_PATH = ""


def part_one(path: str) -> int:
    valves = _read_lines(path)
    for name, valve in valves.items():
        if name == "AA" or valve.rate != 0:
            valve.compute_distances(name, valves)

    valves = {name: valve for name, valve in valves.items() if valve.rate != 0 or name == "AA"}

    def backtrack(path_names: List[str], path_remaining_times: List[int], time: int) -> int:
        # path : name + time needed to go to it
        crt_valve = valves[path_names[-1]]

        for child, dist in crt_valve.distances.items():
            if child in path_names:
                continue
            next_time = time+dist+1
            if next_time > 30:
                continue

            path_names.append(child)
            path_remaining_times.append(30-next_time)
            backtrack(path_names, path_remaining_times, next_time)
            path_names.pop()
            path_remaining_times.pop()

        # Compute pressure
        pressure = 0
        for p, remaining_t in zip(path_names, path_remaining_times):
            pressure += valves[p].rate * remaining_t

        global MAXI_PRESSURE
        global BEST_PATH
        if pressure > MAXI_PRESSURE:
            MAXI_PRESSURE = pressure
            BEST_PATH = "->".join(path_names)

    backtrack(["AA"], [0], 0)
    print(BEST_PATH, MAXI_PRESSURE)

    return MAXI_PRESSURE


def part_two(path: str) -> int:
    rows = _read_lines(path)

    return -1
