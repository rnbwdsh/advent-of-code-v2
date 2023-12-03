import numpy as np

dir_lookup = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

def test_09(data, level):
    snake = np.zeros((10 if level else 2, 2), dtype=int)
    visited = {tuple(snake[0])}
    for line in data:
        dir_letter, amount = line.split(" ")
        for _ in range(int(amount)):
            snake[0] += dir_lookup[dir_letter]  # move head
            for i in range(1, len(snake)):
                dist = snake[i - 1] - snake[i]
                if abs(dist).max() > 1:  # pull head if x or y dist > 1
                    snake[i] += np.sign(dist)  # pull maximally 1/1, -1/1, 1/0...
                visited.add(tuple(snake[-1]))
    return len(visited)
