from typing import List

import numpy as np
import pytest

@pytest.mark.data("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""", 8, 2286)
def test_02(data: List[str], level):
    total_game = 0
    max_per_col = {"red": 12, "green": 13, "blue": 14}
    for line in data:
        game, rest = line.split(":")
        per_col = {"red": 0, "green": 0, "blue": 0}
        game = int(game.replace("Game ", ""))
        for sub in rest.split("; "):
            for p in sub.split(", "):
                num, col = p.strip().split(" ")
                num, col = int(num), col.strip()
                if num > max_per_col[col]:
                    game = None
                per_col[col] = max(per_col[col], num)
        total_game += np.prod(list(per_col.values())) if level else game or 0
    return total_game
