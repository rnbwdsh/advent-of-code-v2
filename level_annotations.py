from functools import partial
from typing import Tuple, List

import aocd.models
import inspect
from aocd import submit, get_data
from numpy import array


def parse(dd, apply, sep):
    if sep is None or sep not in dd:
        return dd
    return array([apply(d) for d in dd.split(sep)])


def run_test(inp, expected, day, level, solver, apply, sep):
    if expected is not None:
        computed = solver(parse(inp, apply, sep), level)
        if not isinstance(computed, str):
            computed = str(computed)
        if not isinstance(expected, str):
            expected = str(expected)
        assert computed == expected, f"Test failed {computed=} != {expected=} with data\n{repr(inp)} for day {day}/{'ab'[level]}"
    print("✓", end=" ")


def level_ab(day: int, test: Tuple | bool = None, levels=(0, 1), quiet=False, sep="\n", apply=lambda a: a):
    # find what folder/year the annotated function is in
    frame = inspect.stack()[1].frame
    filename = frame.f_code.co_filename
    year = filename.split("/")[-2]

    def inner(solver):
        for level in levels:
            # solve with testdata
            if test and (actual := test[1 + level]) is not None:
                run_test(test[0], actual, day, level, solver, apply, sep)
            elif test is None:
                ex = aocd.models.Puzzle(year=year, day=day).examples
                if ex:
                    actual = ex[0].answer_b if level else ex[0].answer_a
                    run_test(ex[0].input_data, actual, day, level, solver, apply, sep)

            # solve real
            sol = solver(parse(get_data(day=day, year=year), apply, sep), level)
            if not isinstance(sol, str):
                sol = str(sol)
            submit(sol, 'ab'[level], day=day, year=year, quiet=quiet)
        return solver  # return the original function, so you can put another annotation on it

    return inner


level_a = partial(level_ab, levels=(0,))
level_b = partial(level_ab, levels=(1,))

