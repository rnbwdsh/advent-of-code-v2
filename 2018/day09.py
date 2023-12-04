from blist import blist

# game params
num_players = 423
last_marble = 71944 * 100

# initialization
m = blist([0, 2, 1])
pos = 1
player = 0
scores = [0] * num_players

for i in range(3, last_marble + 1):
    # print(m)
    # print("pos: ", pos)
    pos += 2
    if pos > len(m):
        pos -= len(m)
    if i % 23 == 0:
        # print("woop")
        pos -= 9  # due to +2
        if pos < 0:
            pos += len(m)
        scores[i % num_players] += m[pos] + i
        m.pop(pos)
    elif pos == len(m):
        m.append(i)
    else:
        m.insert(pos, i)
    if i % 1000000 == 0:
        print(i)
print(max(scores))
