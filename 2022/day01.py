from typing import List

def test_01(data: List[List[int]], level):
    chunks = [sum(chunk) for chunk in data]
    return sum(list(sorted(chunks, reverse=True))[:3]) if level else max(chunks)
