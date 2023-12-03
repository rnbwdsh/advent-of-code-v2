import numpy as np

def test_04(data: str, level):
    numbers, *fields = data.split("\n\n")
    fields = [np.genfromtxt(field.splitlines(), dtype=int) for field in fields]
    winners = set()
    for number in map(int, numbers.split(",")):
        for i in range(len(fields)):
            field = fields[i]
            fields[i][field == number] = -1
            mask = fields[i] == -1
            if (mask.sum(axis=0) == 5).any() or (mask.sum(axis=1) == 5).any():
                winners.add(i)
                if not level or len(winners) == len(fields):
                    return number * field[~mask].sum()
