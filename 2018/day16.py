import copy

def intmap(a, split=","):
    return list(map(int, a.replace("[", "").replace("]", "").split(split)))

class Instruction:
    def __init__(self, mem, opcodes):
        self.OPCODE = opcodes[0]
        self.A = opcodes[1]
        self.B = opcodes[2]
        self.C = opcodes[3]
        self.mem = mem

    def run(self, found):
        instruction = found[self.OPCODE]
        return getattr(self, instruction)();

    # add mul
    def addr(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A] + mem[self.B]
        return mem

    def addi(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A] + self.B
        return mem

    def mulr(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A] * mem[self.B]
        return mem

    def muli(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A] * self.B
        return mem

    # bitwise and/or
    def banr(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A] & mem[self.B]
        return mem

    def bani(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A] & self.B
        return mem

    def borr(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A] | mem[self.B]
        return mem

    def bori(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A] | self.B
        return mem

    # assign, gt, eq
    def setr(self):
        mem = copy.copy(self.mem)
        mem[self.C] = mem[self.A]
        return mem

    def seti(self):
        mem = copy.copy(self.mem)
        mem[self.C] = self.A
        return mem

    def gtir(self):
        mem = copy.copy(self.mem)
        mem[self.C] = int(self.A > mem[self.B])
        return mem

    def gtri(self):
        mem = copy.copy(self.mem)
        mem[self.C] = int(mem[self.A] > self.B)
        return mem

    def gtrr(self):
        mem = copy.copy(self.mem)
        mem[self.C] = int(mem[self.A] > mem[self.B])
        return mem

    def eqir(self):
        mem = copy.copy(self.mem)
        mem[self.C] = int(self.A == mem[self.B])
        return mem

    def eqri(self):
        mem = copy.copy(self.mem)
        mem[self.C] = int(mem[self.A] == self.B)
        return mem

    def eqrr(self):
        mem = copy.copy(self.mem)
        mem[self.C] = int(mem[self.A] == mem[self.B])
        return mem

    def methodList(self, notin=[]):
        funcs = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("_")]
        for n in notin:
            funcs.remove(n)
        return funcs

ind = open("day16.1.txt").read()

counter = 0
total_len = len(ind.split("\n\n"))
for a in ind.split("\n\n"):
    a = a.replace("Before: ", "").replace("After: ", "").split("\n")
    before = intmap(a[0])
    instructions = intmap(a[1], split=" ")
    after = intmap(a[2])

    i = Instruction(before, instructions)
    correct = 0
    for method in method_list:
        result = getattr(i, method)()
        if result == after:
            correct += 1
    if correct >= 3:
        counter += 1
print(counter, "/", total_len)

found = {}
for j in range(10):
    for a in ind.split("\n\n"):
        a = a.replace("Before: ", "").replace("After: ", "").split("\n")
        before = intmap(a[0])
        instructions = intmap(a[1], split=" ")
        after = intmap(a[2])
        if instructions[0] not in found.keys():
            i = Instruction(before, instructions)
            correct = []
            for method in i.methodList(found.values()):
                result = getattr(i, method)()
                if result == after:
                    correct.append(method)
            if len(correct) == 1:
                found[instructions[0]] = correct[0]
print(len(found), found)

ind2 = open("day16.2.txt").read()
mem = [0, 0, 0, 0]
a = [intmap(aa, " ") for aa in ind2.split("\n")]
for instruction in a:
    i = Instruction(mem, instruction)
    mem = i.run(found)
print(mem)
