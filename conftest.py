from typing import Callable, List, Tuple, Any
import re

from _pytest.config import hookimpl
from _pytest.fixtures import SubRequest, fixture
from _pytest.mark import Mark
from _pytest.python import Function
from aocd.models import Puzzle

from parsers import TYPE_PARSER

class Example:
    def __init__(self, input_data, answer_a, answer_b):
        self.input_data = input_data
        self.answer_a = answer_a
        self.answer_b = answer_b

def make_str(v: Any):
    return str(v) if not isinstance(v, str) else v

def run_example(func: Callable, input_data: str, expected: Example, level: int, parser: Callable):
    inp = parser(input_data)
    answer = func(inp, level)
    assert make_str(answer) == make_str(expected), f"Failed test:\n{answer=}\n{expected=}"

def run_real(func, puzzle, level, parser):
    inp = parser(puzzle.input_data)
    answer = func(inp, level)
    if (level and puzzle.answered_b) or puzzle.answered_a:
        assert (puzzle.answer_b if level else puzzle.answer_a) == make_str(answer)
    else:
        setattr(puzzle, f"answer{'_b' if level else '_a'}", answer)

def wrap_func(func, markers: List[Mark], puzzle: Puzzle, level: int, **_):
    def wrapper(*_, **__):  # *_ / **_ is to ignore arguments
        parser = TYPE_PARSER[func.__annotations__.get("data", None)]
        examples = puzzle.examples
        for m in markers:
            if m.name == "data":
                data, part_a, part_b = m.args
                examples = [Example(data[0], part_a, None), Example(data[1], None, part_b)] \
                    if isinstance(data, Tuple) else [Example(data, part_a, part_b)]

        if [m.name for m in markers].count("notest") == 0:
            for example in examples:
                if expected := example.answer_b if level else example.answer_a:
                    run_example(func, example.input_data, expected, level, parser)
        run_real(func, puzzle, level, parser)

    return wrapper

@fixture
def data(request: SubRequest):
    day = int(request.fspath.purebasename.replace("day", "")[:2])  # noqa
    year = int(request.fspath.dirpath().basename)  # noqa
    request.node.funcargs["puzzle"] = Puzzle(year=year, day=day)

@fixture(params=[0, 1])
def level(request: SubRequest) -> int:
    if "level_a" in request.node.fixturenames:
        return 0
    elif "level_b" in request.node.fixturenames:
        return 1
    return request.param

@fixture
def level_a(level: int, request: SubRequest): pass  # noqa, dummy fixtures to only run one level

@fixture
def level_b(level: int, request: SubRequest): pass  # noqa, dummy fixtures to only run one level

@hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem: Function):
    if re.match(r"test_\d?\d", pyfuncitem.function.__name__):
        pyfuncitem.funcargs["markers"] = pyfuncitem.own_markers
        pyfuncitem.obj = wrap_func(pyfuncitem.obj, **pyfuncitem.funcargs)
    yield
