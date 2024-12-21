import functools
from typing import List, Tuple

import pytest

class Keypad:
    layout = ["789", "456", "123", " 0A"]
    def __init__(self, pos=3 + 2j, so_far=""):
        self.pos = pos
        self.so_far = so_far

    def in_bounds(self):
        return 0 <= self.pos.real < len(self.__class__.layout) and 0 <= self.pos.imag < len(self.__class__.layout[0]) and self.button_at() != " "

    def button_at(self) -> str:
        return self.__class__.layout[int(self.pos.real)][int(self.pos.imag)]

    def solve(self, press: str) -> set[str]:
        # otherwise, it tries to go up + down
        if press == "A":
            return {"A"}
        curr = [self]
        while press:
            curr_next = []
            success = 0
            for c in curr:
                for k, v in {'^': -1, 'v': 1, '<': -1j, '>': 1j}.items():
                    cc = c.copy_move_keypad(k, v)
                    if cc is None:
                        continue
                    if cc.button_at() == press[0]:
                        success = 0
                        for next_letter in press:
                            if next_letter == press[0]:
                                cc.so_far += "A"
                                success += 1
                            else:
                                break
                    curr_next.append(cc)
            if success:
                # hack: if you want to do the same char multiple times,
                curr_next = [t for t in curr_next if t.so_far.endswith("A")]
                press = press[success:]
            curr = curr_next
        return set([c.so_far for c in curr])

    def copy_move_keypad(self, letter, direction):
        c = self.__class__(self.pos, self.so_far)
        c.pos += direction
        c.so_far += letter
        if not c.in_bounds():
            return None
        return c


class Dpad(Keypad):
    layout = [" ^A", "<v>"]
    def __init__(self, pos = 2j, so_far =""):
        super().__init__(pos, so_far)


@functools.cache
def dpad_cached(s: str) -> set[str]:
    assert s[-1] == "A"
    return Dpad().solve(s)

def yield_chunks(s: str) -> Tuple[str, str]:
    """ Split every keypad action into sub-actions that end with A"""
    while s:
        end = s.find("A") + 1
        yield s[:end]
        s = s[end:]

@functools.cache
def tree_replace_resolve(s: str, depth = 2) -> List | int:
    if depth == 0:
        return len(s)
    return sum([min([tree_replace_resolve(chunk, depth - 1)
                     for chunk in dpad_cached(chunk)])
                for chunk in yield_chunks(s)])

@pytest.mark.data("""029A
980A
179A
456A
379A""", 126384, None)
def test_20(data: List[str], level):
    repeat = 25 if level else 2
    return sum(int(line[:3]) * min(tree_replace_resolve(k, repeat)
                                   for k in Keypad().solve(line))
               for line in data)

def test___tree():
    example = "<A^A>^^AvvvA"
    assert Keypad().solve("029A") == {example, "<A^A^>^AvvvA", "<A^A^^>AvvvA"}
    assert "v<<A>>^A<A>AvA<^AA>A<vAAA>^A" in Dpad().solve(example)
    assert tree_replace_resolve(example, 2) == 68
