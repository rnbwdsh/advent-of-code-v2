import re

import numpy as np
import pytest

@pytest.mark.data("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""", 4361, 467835)
def test_03(data: np.ndarray, level):
    symbols = set("*") if level else set("".join(data.flatten())) - set(".0123456789")

    # mask in all symbols and their neighbors, as well as numbers next to those
    mask = mask_in_around_symbols(data, symbols)
    masked = np.full(data.shape, ".", dtype=str)
    masked[mask] = data[mask]

    if level:
        return sum(gen_mul_adjacent(data, replace_connected(data, masked)))
    else:
        joined = ".".join(["".join(row) for row in masked])
        return sum([int(n) for n in re.findall(r"\d+", joined)])

def replace_connected(field, masked):
    replaced = np.zeros(field.shape, dtype=int)
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            num = 0
            for y_end in range(y, len(masked[x])):
                if replaced[x, y_end] == 0 and masked[x, y_end].isdigit():
                    num = num * 10 + int(masked[x, y_end])
                    replaced[x, y:y_end + 1] = num
                else:
                    break
    return replaced

def mask_in_around_symbols(field, symbols):
    mask = np.full(field.shape, False)
    for x, y in np.ndindex(field.shape):
        if field[x, y] in symbols:
            mask[x - 1:x + 2, y - 1:y + 2] = True

    # mask in all left/right neighbors of masked in numbers
    for x, y in np.ndindex(field.shape):
        if mask[x, y] and field[x, y].isdigit():
            expand_digit_mask_at(field, mask, x, y)
    return mask

def expand_digit_mask_at(field, mask, x, y):
    # iterate to the right first
    for r in [range(y, min(y + 5, field.shape[1])), reversed(range(max(y - 5, 0), y))]:
        for y_end in r:
            if not field[x, y_end].isdigit():
                break
            mask[x, y_end] = True

def gen_mul_adjacent(field, replaced):
    for x, y in zip(*np.nonzero(field == "*")):  # noqa # numpy.__eq__ is checked wrongly
        surrounding = set(list(replaced[x - 1:x + 2, y - 1:y + 2].flatten())) - {0}
        if len(surrounding) == 2:
            yield np.prod(list(surrounding))
