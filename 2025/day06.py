from typing import List

import numpy as np
import pytest


def combine(numbers: List[int], sign: str):
    if sign == '*':
        return np.prod(numbers)
    elif sign == '+':
        return np.sum(numbers)
    raise ValueError(f"Unknown sign: {sign}")


@pytest.mark.data('''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  ''', 4277556, 3263827)
def test_06(data: List[str], level):
    total = 0
    # split by " +" and create np array
    if not level:
        grid = [[int(x) for x in row.split()] for row in data[:-1]]
        signs = data[-1].split()
        for col in range(len(grid[0])):
            total += combine([grid[row][col] for row in range(len(grid))], signs[col])
    else:
        data = np.array([list(d) for d in data], dtype=str)
        x_last = 0
        columns = []
        signs = []
        for x in range(len(data[0])):
            if all(data[y, x] == ' ' for y in range(len(data))):
                columns.append(data[:-1, x_last:x].T)
                signs.append(data[-1, x_last])
                x_last = x+1
        columns.append(data[:-1, x_last:].T)
        signs.append(data[-1, x_last])
        for col, sign in zip(columns, signs):
            total += combine([int(''.join(row).strip()) for row in col], sign)
    return total
