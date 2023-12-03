import itertools

import numpy as np

ROCKS = ['####', '.#.\n###\n.#.', '..#\n..#\n###', '#\n#\n#\n#', '##\n##']
WIDTH, PADDING_W, PADDING_H, SIM_TIME = 7, 2, 3, 1_000_000_000_000

def test_17(data, level):
    mul = 3 if level else 1  # given by assignment
    operations = itertools.cycle(data[0])  # generator that infinitely yields signs

    # create a big field with a floor
    field = np.zeros((WIDTH, 4000 * mul), dtype=int)
    field[:, 0] = 1

    # track gains per round
    last_height = 1
    diffs = []
    for block_nr in range(2022 * mul):
        block = ROCKS[block_nr % len(ROCKS)]
        block = np.rot90(np.array([[int(c == "#") for c in line] for line in block.split("\n")]), k=3)
        block_x = PADDING_W
        curr_height = np.argwhere(field.sum(axis=0) == 0)[0][0]  # get highest pos
        block_y = curr_height + PADDING_H
        block_w, block_h = block.shape

        # for level 1, we need the gain per round
        diffs.append(curr_height - last_height)
        last_height = curr_height

        while True:  # simulate falling, then l/r
            def check_collision():  # parametrize via scope
                return (field[block_x:block_x + block_w, block_y:block_y + block_h] * block).sum() > 0

            if check_collision():
                # blocks would overlap, so stop dropping
                field[block_x:block_x + block_w, block_y + 1:block_y + 1 + block_h] += block
                break

            op_dir = -1 if next(operations) == "<" else 1
            block_x += op_dir
            if block_x < 0 or (block_x + block_w) > WIDTH or check_collision():
                block_x -= op_dir  # go back
            block_y -= 1  # otherwise, you you need modified collision detection

    if level:
        offset = period_len = 0  # to disable some warnings
        for offset, period_len in itertools.product(range(1000), range(20, 2000)):  # single loop easier to break
            if diffs[offset:offset + period_len] == diffs[offset + period_len:offset + period_len * 2]:
                break  # offset and corr_len are now set
        before = sum(diffs[:offset])
        period = diffs[offset:offset + period_len]
        period_num = (SIM_TIME - offset) // period_len
        after_num = ((SIM_TIME - offset) % period_len) + 1  # +1 because range is exclusive
        after = sum(period[:after_num])
        return before + period_num * sum(period) + after
    else:
        return np.argwhere(field.sum(axis=0) == 0)[0][0] - 1
