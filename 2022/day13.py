from typing import List, Optional

def compare(a: int | List, b: int | List) -> Optional[bool]:
    if isinstance(a, int) and isinstance(b, int):
        if a == b:  # Otherwise, the inputs are the same integer
            return None  # continue checking the next part of the input.
        return a < b  # both values are integers, the lower integer should come first
    elif isinstance(a, int):  # If exactly one value is an integer, convert the integer to a
        return compare([a], b)  # list which contains that integer as its only value, then retry the comparison
    elif isinstance(b, int):
        return compare(a, [b])
    elif isinstance(a, list) and isinstance(b, list):  # If both values are lists
        for i in range(len(a)):  # compare the first value of each list, then the second value, and so on.
            if i == len(b):
                return False  # If the right list runs out of items first, the inputs are not in the right order
            if (res := compare(a[i], b[i])) is not None:
                return res
        if len(a) == len(b):  # If the lists are the same length and no comparison makes a decision about the order
            return None  # continue checking the next part of the input
        return True  # If the left list runs out of items first, the inputs are in the right order

def bubble_sort(data):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if not compare(data[i], data[j]):
                data[i], data[j] = data[j], data[i]
    return data

def test_13(data: List[List[str]], level):
    valid_chunks = []
    if level:
        data = [",".join(line) for line in data]
        data = list(eval(",".join(data))) + [[2], [6]]
        bubble_sort(data)
        return (data.index([2]) + 1) * (data.index([6]) + 1)
    else:
        for i, line in enumerate(data):
            data = eval(",".join(line))
            if compare(*data):
                valid_chunks.append(i + 1)
    return sum(valid_chunks)
