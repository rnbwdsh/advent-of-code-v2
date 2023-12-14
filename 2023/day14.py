import numpy as np
import pytest

@pytest.mark.data("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""", 136, 64)
def test_14(data: np.ndarray, level):
    if level:
        seen = ["".join(data.flatten())]
        seen_at = [data]
        for time in range(1000):
            for _ in range(4):   # north, west, south, east. up is -1
                data = roll_north(data)
                data = np.rot90(data, -1)
            after = "".join(data.flatten())
            if after in seen:
                first_repetition = seen.index(after)
                period = time - first_repetition + 1
                data = seen_at[first_repetition + (1_000_000_000 - first_repetition) % period]
                break
            seen_at.append(data)
            seen.append(after)
    else:  # roll north once
        data = roll_north(data)
    return sum(sum(row == "O") * (len(data) - ri) for ri, row in enumerate(data))

def roll_north(field: np.ndarray) -> np.ndarray:
    f = field.copy()
    before = np.zeros_like(f)
    while not np.all(np.equal(before, f)):  # shift up until nothing changes
        for row, col in np.argwhere(f == "O"):
            for _ in range(row):  # max number of shifting up is row
                row_above = row - 1
                if 0 <= row_above and f[row, col] == "O" and f[row_above, col] == ".":
                    f[row_above, col] = "O"
                    f[row, col] = "."
                    row = row_above
                else:
                    break
        before = f.copy()
    return f
