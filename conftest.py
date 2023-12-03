from typing import Tuple, Callable, List

from _pytest.config import hookimpl
from _pytest.fixtures import SubRequest, fixture
from _pytest.mark import Mark
from _pytest.python import Function
from aocd.models import Puzzle

def parse_chunks_int(data: str) -> List[List[int]]:
    return [parse_line_int(line) for line in data.split("\n\n")]

def parse_line_int(data: str) -> List[int]:
    split_chars = set(data) - set("-0123456789")
    split_char = list(split_chars)[0] if split_chars else "\n"
    return [int(i) for i in data.split(split_char)]

def parse_line(data: str) -> List[str]:
    return data.split("\n\n" if "\n\n" in data else "\n")

def parse_chunks(data: str) -> List[List[str]]:
    return [parse_line(line) for line in data.split("\n\n")]

TYPE_PARSER = {
    List[List[int]]: parse_chunks_int,
    List[List[str]]: parse_chunks,
    List[int]: parse_line_int,
    List[str]: parse_line,
    str: lambda d: d,
    None: lambda d: d.split("\n"),
    int: int,
}

def run_example_test(func: Callable, puzzle: Puzzle, level: int, parser: Callable):
    example = puzzle.examples[0]
    expected = example.answer_b if level else example.answer_a
    if expected:
        inp = parser(example.input_data)
        answer = func(inp, level)
        if not isinstance(answer, str):
            answer = str(answer)
        assert answer == expected, f"Failed test:\n{answer=}\n{expected=}"

def run_real(func, puzzle, level, parser):
    inp = parser(puzzle.input_data)
    answer = func(inp, level)
    if level:
        puzzle.answer_b = answer
        assert puzzle.answered_b, f"Wrong answer\n{answer=}"
    else:
        puzzle.answer_a = answer
        assert puzzle.answered_a, f"Wrong answer\n{answer=}"

def wrap_func(func, markers: List[Mark], puzzle: Puzzle, level: int, **_):
    def wrapper(*_, **__):
        parser = TYPE_PARSER[func.__annotations__.get("data", None)]
        if [m.name for m in markers].count("notest") == 0:
            run_example_test(func, puzzle, level, parser)
        run_real(func, puzzle, level, parser)

    return wrapper

@fixture
def data(request: SubRequest):
    day = int(request.fspath.purebasename.replace("day", ""))  # noqa
    year = int(request.fspath.dirpath().basename)  # noqa
    request.node.funcargs["puzzle"] = Puzzle(year=year, day=day)

@fixture(params=[0, 1])
def level(request: SubRequest) -> int:
    if "level_a" in request.node.fixturenames:
        return 0
    elif "level_b" in request.node.fixturenames:
        return 1
    return request.param

# dummy fixtures to only run one level
@fixture
def level_a(level: int, request: SubRequest): pass

@fixture
def level_b(level: int, request: SubRequest): pass

@hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem: Function):
    pyfuncitem.funcargs["markers"] = pyfuncitem.own_markers
    pyfuncitem.obj = wrap_func(pyfuncitem.obj, **pyfuncitem.funcargs)
    yield
