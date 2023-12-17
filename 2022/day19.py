import functools
import operator
import re
from functools import partial
from multiprocessing import Pool

import numpy as np
import pytest

RESOURCES = ["ore", "clay", "obsidian", "geode"]
MUL = np.array([8 ** i for i in range(8)], dtype=np.int64)

@pytest.mark.notest
def test_19(data, level):
    res = Pool(32).map(partial(run_simulation, level=level), data[:3] if level else data)
    return functools.reduce(operator.mul, res) if level else sum([r * i for i, r in enumerate(res, 1)])

def forward(states, blueprint_line):
    state_next = states + blueprint_line  # try build
    valid_mask = state_next.min(axis=1) >= 0  # filter out steps that lead to negative resources
    state_next[:, :4] += states[:, 4:]  # add output of factories to inventory, after checking
    return state_next[valid_mask]

def run_simulation(line, level):
    # create blueprints and states as 8-vectors of [*inventory, *factory]
    blueprint = np.zeros((5, 8), dtype=np.int8)
    for cost_line in line.split("Each ")[1:]:
        buy_resource = cost_line.split(" ")[0]
        for buy_price in re.findall(r"\d+ \w+", cost_line):
            resource_price, resource_type = buy_price.split()
            blueprint[RESOURCES.index(buy_resource), RESOURCES.index(resource_type)] = -int(
                resource_price)  # sub resources
        blueprint[RESOURCES.index(buy_resource), 4 + RESOURCES.index(buy_resource)] = 1  # add one building
    cost_build_all = blueprint[:, :3].sum(axis=0)

    # batch-process everything in a timestep at once
    states = np.array([[0, 0, 0, 0, 1, 0, 0, 0]])
    for _ in range(32 if level else 24):
        geode_count = states[:, 3].max()
        states = np.concatenate([forward(states, blueprint_line) for blueprint_line in blueprint])
        states = states[np.unique(states @ MUL, return_index=True)[
            1]]  # trim duplicates, by making and reducing a 1d array (regular np.unique is sloooooow)
        states = states[(states[:, :3] + cost_build_all).min(axis=1) < 0]  # trim states that save too many resources
        states = states[states[:, 3] >= geode_count]  # trim states that don't have the max geode count
    return int(states[:, 3].max())