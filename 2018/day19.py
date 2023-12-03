#!/usr/bin/env python
# coding: utf-8

# In[14]:


reg = [0, 0, 0, 0, 0, 0]
a = """seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""
IPADDR = 0
a = """addi 4 16 4
seti 1 7 2
seti 1 1 5
mulr 2 5 3
eqrr 3 1 3
addr 3 4 4
addi 4 1 4
addr 2 0 0
addi 5 1 5
gtrr 5 1 3
addr 4 3 4
seti 2 7 4
addi 2 1 2
gtrr 2 1 3
addr 3 4 4
seti 1 3 4
mulr 4 4 4
addi 1 2 1
mulr 1 1 1
mulr 4 1 1
muli 1 11 1
addi 3 3 3
mulr 3 4 3
addi 3 9 3
addr 1 3 1
addr 4 0 4
seti 0 1 4
setr 4 9 3
mulr 3 4 3
addr 4 3 3
mulr 4 3 3
muli 3 14 3
mulr 3 4 3
addr 1 3 1
seti 0 6 0
seti 0 7 4"""
IPADDR = 4
instr = ["seti", "setr", "addi", "addr", "muli", "mulr", "eqrr", "gtrr"]
a = [aa.split() for aa in a.split("\n")]
for i in range(len(a)):
    a[i] = [instr.index(a[i][0])] + list(map(int, a[i][1:]))
prog = a

while reg[0] < len(prog):
    instr, a, b, c = prog[reg[IPADDR]]

    # print("regs:", reg)
    # print("before", prog[reg[IPADDR]])

    if instr == 0:
        reg[c] = a
    elif instr == 1:
        reg[c] = reg[a]
    elif instr == 2:
        reg[c] = reg[a] + b
    elif instr == 3:
        reg[c] = reg[a] + reg[b]
    elif instr == 4:
        reg[c] = reg[a] * b
    elif instr == 5:
        reg[c] = reg[a] * reg[b]
    elif instr == 6:
        reg[c] = int(reg[a] == reg[b])
    elif instr == 7:
        reg[c] = int(reg[a] > reg[b])
    else:
        print("unknown instruction", instr)
    # if reg[1] == 10551311:
    #    reg[1] = 10551311//100

    reg[IPADDR] += 1

reg[IPADDR] -= 1
print("regs:", reg)

# In[16]:


# loop counter is 10551311
# so we hook it to set it to smth different

# result with 911 (ex1): 912
# result with //50000: 211: 212
# result with //10000: 1055: 217
# result with // 5000: 2100: 219
# result with // 2000: 5275: 242
# result with // 1500: 7034: 3520
# result with // 1000: 10551: 3521
# result with //  500: 21102: 3529
# result with //  100: 105513: 140688
# so number * 5 -> +5

# toolow: 3530

from functools import reduce

def factors(n):
    return set(reduce(list.__add__,
                      ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))

print(factors(10551311))
print(sum(factors(10551311)))
