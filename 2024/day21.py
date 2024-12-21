from functools import cache
from itertools import takewhile
from typing import List

import pytest

class Keypad:
    layout = ["789", "456", "123", " 0A"]

    def __init__(self, pos=3 + 2j, so_far=""):
        self.pos = pos
        self.so_far = so_far

    def __call__(self, press: str) -> set[str]:
        """ modified DFS with repetition action """
        if press == "A":
            return {"A"}
        curr = [self]
        while press and curr:
            curr_next, found = self.find_inner(curr, press)
            if found:
                curr_next = [c for c in curr_next if c.so_far.endswith("A")]
                press = press[found:]
            curr = curr_next
        return set([c.so_far for c in curr])

    def find_inner(self, curr, press):
        dir_items = {'^': -1, 'v': 1, '<': -1j, '>': 1j}.items()
        curr_next = []
        found = 0
        for k, v in dir_items:
            for c in curr:
                cpy = self.__class__(c.pos + v, c.so_far + k)
                if cpy.button_at() == ' ':
                    continue
                if cpy.button_at() == press[0]:
                    # if the same button has to be pressed multiple times, we just repeatedly press A
                    found = sum(1 for _ in takewhile(lambda x: x == press[0], press))
                    cpy.so_far += "A" * found
                curr_next.append(cpy)
        return curr_next, found

    def button_at(self) -> str:
        row, col = int(self.pos.real), int(self.pos.imag)
        if 0 <= row < len(self.layout) and 0 <= col < len(self.layout[0]):
            return self.layout[row][col]
        return " "

class Dpad(Keypad):
    layout = [" ^A", "<v>"]

    def __init__(self, pos=2j, so_far=""):
        super().__init__(pos, so_far)

@cache
def tree_fold(s: str, depth) -> List | int:
    """ build and consume a recursive substitution tree to find the shortest substitution """
    if depth == 0:
        return len(s)
    return sum(min(tree_fold(solved_chunk, depth - 1) for solved_chunk in Dpad()(chunk + "A"))
               for chunk in s.split("A")[:-1])

@pytest.mark.data("029A\n980A\n179A\n456A\n379A", 126384, None)
def test_20(data: List[str], level):
    repeat = 25 if level else 2
    return sum(int(line[:3]) * min(tree_fold(k, repeat) for k in Keypad()(line))
               for line in data)

def test_keypad_dpad_tree():
    example = "<A^A>^^AvvvA"
    assert Keypad().__call__("029A") == {example, "<A^A^>^AvvvA", "<A^A^^>AvvvA"}
    assert "v<<A>>^A<A>AvA<^AA>A<vAAA>^A" in Dpad()(example)
    assert tree_fold(example, 2) == 68
