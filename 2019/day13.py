from typing import List

import numpy as np

from computer import Computer

BLOCK, PAD, BALL = 2, 3, 4

def play_game(data):
    p = Computer([2] + data[1:])  # set d[0] = 2 to insert 2 coins
    pos_ball = pos_pad = 0  # just for step 0
    score = 0
    while not p.done:
        output = p.compute([np.sign(pos_ball - pos_pad)])
        # display routine: draw tile @ x/y if x/y is not -1/0 and remember pos_ball/hpad
        for i in range(0, len(output), 3):
            x, y, tile = output[i:i + 3]
            if x == -1 and y == 0:
                score = tile
            else:
                if tile == BALL:
                    pos_ball = x
                elif tile == PAD:
                    pos_pad = x
    return score

def test_13(data: List[int], level):
    p = Computer(data)
    prog_out = np.array(p.compute([]))
    # select every 3rd block and count how many are type block
    return play_game(data) if level else sum(np.equal(prog_out[range(2, len(prog_out), 3)], 2))
