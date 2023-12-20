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
        targets = targets.split(", ")
        if name == "broadcaster" or name[0] not in "%&":
            modules[name] = Broadcast(name, targets)
        elif name[0] == "%":
            modules[name[1:]] = FlipFlop(name[1:], targets)
        elif name[0] == "&":
            modules[name[1:]] = Conjunction(name[1:], targets)

    # initialize conjunctions
    for targets in modules.values():
        for t in targets.followers:
            if t in modules:
                if isinstance(modules[t], Conjunction):
                    modules[t].input_memory[targets.name] = False
            elif level:
                monitor = targets
    try:
        monitor.hist = {k: 0 for k in monitor.input_memory}  # noqa name error
    except NameError:
        pass

    cnt = [0, 0]
    try:
        for btn_num in range(1, 10_000_000 if level else 1001):
            todo = [Signal("button", False, "broadcaster")]
            while todo:
                sig = todo.pop(0)
                cnt[sig.high] += 1

                if rcv := modules.get(sig.receiver, None):
                    todo.extend(rcv.pulse(sig.sender, sig.high, btn_num))
        return cnt[0] * cnt[1]
    except RuntimeError as e:
        return e.args[0]

Signal = namedtuple("Signal", "sender high receiver")

@dataclass
class Broadcast:
    name: str
    followers: List[str]

    def pulse(self, _, high, __):
        return [Signal(self.name, high, f) for f in self.followers]

@dataclass
class FlipFlop(Broadcast):
    state = False

    def pulse(self, sender, high, btn_press):
        if high:
            return []
        else:
            self.state = not self.state
            return super().pulse(sender, self.state, btn_press)

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
                raise RuntimeError(lcm(*self.hist.values()))
        return super().pulse(sender, not all(self.input_memory.values()), btn_press)
