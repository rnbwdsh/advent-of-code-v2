import numpy as np
import pytest

DIR = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}


def can_push(a: np.array, x: int, y: int, dx: int, dy: int) -> bool:
    x += dx
    y += dy
    if a[x, y] == '#':
        return False
    elif a[x, y] == ".":
        return True
    if dx != 0 and a[x, y] in "[]":
        return can_push(a, x, y, dx, dy) and can_push(a, x, y + (1 if a[x, y] == "[" else -1), dx, dy)
    return can_push(a, x, y, dx, dy)


def push(a: np.array, px: int, py: int, dx: int, dy: int, prev: str):
    curr = a[px, py]
    a[px, py] = prev
    x, y = px + dx, py + dy
    if a[x, y] == '.':
        a[x, y] = curr
        return
    if dx != 0 and a[x, y] in "[]":
        push(a, x, y + (1 if a[x, y] == "[" else -1), dx, dy, ".")
    push(a, x, y, dx, dy, curr)



def simulate(a: np.array, moves: str) -> np.array:
    pos = np.where(a == '@')
    x, y = (pos[0][0], pos[1][0])
    for move in moves:
        if move == "\n":
            continue
        dx, dy = DIR[move]
        if can_push(a, x, y, dx, dy):
            push(a, x, y, dx, dy, ".")
            x += dx
            y += dy
    return a


@pytest.mark.data("""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""", 10092, 9021)
def test_15(data: str, level):
    data, moves = data.split('\n\n')
    if level:
        data = data.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
    data = np.array([list(i) for i in data.split('\n')])
    res = simulate(data, moves)
    return sum(100 * i1 + j for (i1, j), val in np.ndenumerate(res) if val in {'O', '['})
