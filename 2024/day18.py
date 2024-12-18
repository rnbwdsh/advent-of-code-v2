import networkx
import pytest
from typing import List


@pytest.mark.data("""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""", 22, "6,1")
def test_18(data: List[str], level):
    is_test = data[0] == "5,4"
    size = 7 if is_test else 71
    if is_test:
        grid = networkx.grid_2d_graph(size, size)
    else:
        grid = networkx.grid_2d_graph(size, size)
    if level:
        # find the first byte that cuts you off from the end
        for i, line in enumerate(data):
            x, y = map(int, line.split(","))
            grid.remove_node((x, y))
            try:
                networkx.shortest_path_length(grid, (0, 0), (size-1, size-1))
            except networkx.exception.NetworkXNoPath:
                return f"{x},{y}"
    else:
        for line in data[:(12 if is_test else 1024)]:
            x, y = map(int, line.split(","))
            grid.remove_node((x, y))
        return networkx.shortest_path_length(grid, (0, 0), (size-1, size-1))
