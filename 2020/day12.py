from level_annotations import level_ab

dire = {"N": 1, "S": -1, "E": 1j, "W": -1j}
turn = {"L": -1j, "R": 1j}

@level_ab(12)
def solve(data, method=0):
    pos, wp = 0, 1 + 10j if method else 1j
    for line in data:
        cmd, dist = line[0], int(line[1:])
        if cmd in dire:
            if method:
                wp += dist * dire[cmd]
            else:
                pos += dist * dire[cmd]
        elif cmd == "F":
            pos += dist * wp
        elif cmd in turn:
            wp *= turn[cmd] ** (dist // 90)
        # print("cmd", line, "pos", pos, "facing", facing)
    return int(abs(pos.real) + abs(pos.imag))
