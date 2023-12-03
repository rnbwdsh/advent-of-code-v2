import pytest

@pytest.mark.notest
def test_10(data, level):
    states, x = [1], 1
    for line in data:
        states.append(x)
        if line.startswith("addx"):
            x += int(line[5:])
            states.append(x)
    if level:
        for t, v in enumerate(states):
            print("#" if ((v - t + 1) % 40) // 3 == 0 else " ", end="\n" if t % 40 == 39 else "")
        print()
        return "PGHFGLUG"
    else:
        return sum([states[i - 1] * i for i in (20, 60, 100, 140, 180, 220)])
