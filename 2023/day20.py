from collections import namedtuple
from dataclasses import dataclass, field
from math import lcm
from typing import List, Dict, Optional

import pytest

@pytest.mark.data("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""", 32000000, None)
def test_20(data: List[str], level):
    modules = {}
    for line in data:
        name, targets = line.split(" -> ")
        constructor = {"b": Broadcast, "%": FlipFlop, "&": Conjunction}[name[0]]
        modules[name[1:]] = constructor(name[1:], targets.split(", "))
    # initialize conjunctions
    for targets in modules.values():
        for t in targets.followers:
            if t in modules:
                if isinstance(modules[t], Conjunction):
                    modules[t].input_memory[targets.name] = False
            else:
                monitor = targets
    if level:
        monitor.hist = {k: 0 for k in monitor.input_memory}  # noqa name error

    # main loop
    cnt = [0, 0]
    for btn_num in range(1, 10_000_000 if level else 1001):
        todo = [Signal("button", False, "roadcaster")]
        while todo:
            sig = todo.pop(0)
            cnt[sig.high] += 1  # count low/high signals
            if rcv := modules.get(sig.receiver, None):
                try:
                    nx = rcv.pulse(sig.sender, sig.high, btn_num)
                    todo.extend(nx)
                except TypeError:
                    return nx
    return cnt[0] * cnt[1]

Signal = namedtuple("Signal", "sender high receiver")

@dataclass
class Broadcast:
    name: str
    followers: List[str]

    def _pulse(self, high):
        return [Signal(self.name, high, f) for f in self.followers]

    def pulse(self, _, high, __):
        return self._pulse(high)

@dataclass
class FlipFlop(Broadcast):
    state = False

    def pulse(self, sender, high, btn_press):
        if high:
            return []
        else:
            self.state = not self.state
            return self._pulse(self.state)

@dataclass
class Conjunction(Broadcast):
    input_memory: Dict[str, bool] = field(default_factory=dict)
    hist: Optional[Dict[str, int]] = None

    def pulse(self, sender, high, btn_press):
        self.input_memory[sender] = high
        if self.hist:
            for k, v in self.input_memory.items():
                if v and not self.hist[k]:
                    self.hist[k] = btn_press
            if all(self.hist.values()):  # raise RuntimeError if we are done, containing the result
                return lcm(*self.hist.values())
        return self._pulse(not all(self.input_memory.values()))
