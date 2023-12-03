import numpy as np

from level_annotations import level_ab

@level_ab(11)
def test(lines, level):
    data = np.pad([[int(i) for i in line] for line in lines], (1, 1), constant_values=-99999)
    total = 0

    for step in range(99999 if level else 100):
        data += 1  # increase every field value by 1
        flashed_this_step = set()
        while data[data > 9].any():  # inner step has to be redone to propagate it
            for x, y in zip(*np.where(data > 9)):  # for all values > 9
                data[x - 1:x + 2, y - 1:y + 2] += 1  # increase adjacent values +1
                flashed_this_step.add((x, y))
            for x, y in flashed_this_step:  # reset after every sub-step, so it can't re-flash as the max number of neigh is 9
                data[x, y] = 0
        total += len(flashed_this_step)
        if level and len(flashed_this_step) == 100:
            return step + 1
    return total
