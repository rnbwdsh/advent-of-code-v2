import numpy as np

def drop_sand(grid: np.array, x: int = 500, y: int = 0) -> bool:
    for y in range(y, grid.shape[1] - 1):
        if grid[x, y] == "." and grid[x, y + 1] in "#o":
            if grid[x - 1, y + 1] == ".":  # try left
                return drop_sand(grid, x - 1, y + 1)
            elif grid[x + 1, y + 1] == ".":  # try right
                return drop_sand(grid, x + 1, y + 1)
            else:  # straight drop
                grid[x, y] = "o"
                return True
    return False  # dropped out of the grid

def test_14(data, level):
    field = np.full((1000, 200), ".")
    highest_y = 0
    for line in data:
        line_parts = [[int(s) for s in p.split(",")] for p in line.split(" -> ")]
        for (x, y), (xn, yn) in zip(line_parts, line_parts[1:]):
            field[x, y] = field[xn, yn] = "#"
            if x == xn:
                field[xn, min(yn, y):max(yn, y)] = "#"
            else:
                field[min(xn, x):max(xn, x), yn] = "#"
            highest_y = max(yn, highest_y)
    if level:
        field[:, highest_y + 2] = "#"  # draw "floor"
    while drop_sand(field, 500, 0) and field[500, 0] == ".":
        pass
    return (field == "o").sum()
