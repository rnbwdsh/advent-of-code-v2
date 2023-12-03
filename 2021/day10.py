score0 = {")": 3, "]": 57, "}": 1197, ">": 25137}
score1 = {")": 1, "]": 2, "}": 3, ">": 4}
close = {")": "(", "]": "[", "}": "{", ">": "<"}
score1 = {v: score1[k] for k, v in close.items()}

def test_10(data, level):
    total = 0
    scores = []
    for line in data:
        opened = []
        for char in line:
            if char in close:
                if opened and opened[-1] == close[char]:
                    opened.pop(-1)
                else:  # error case: no closing tag on stack
                    total += score0[char]
                    break
            else:
                opened += char
        else:  # if no break was taken
            subtotal = 0
            for c in reversed(opened):
                subtotal = subtotal * 5 + score1[c]
            scores.append(subtotal)
    return sorted(scores)[len(scores) // 2] if level else total
