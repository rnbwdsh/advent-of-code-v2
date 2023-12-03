from operator import gt, lt, eq

import numpy as np
from bitstring import BitStream

from level_annotations import level_ab

OPERATORS = {0: sum, 1: np.prod, 2: min, 3: max, 5: lambda a: gt(*a), 6: lambda a: lt(*a), 7: lambda a: eq(*a)}
LITERAL_TYPEID = 4
CHUNK_SIZE = 4
LEN_CNT = 11
LEN_BITS = 15

def parse(packet: BitStream):
    version = packet.read(3).uint
    typeid = packet.read(3).uint

    if typeid == LITERAL_TYPEID:
        val = 0
        read_more = True
        while read_more:  # read chunks of 1+4 = 5 until a chunk starts with 1
            read_more = packet.read(1)
            val = packet.read(CHUNK_SIZE).uint + (val << CHUNK_SIZE)
    else:  # operator
        val = []  # list of sub-packet-values
        length_type = packet.read(1)  # 0: bits, 1: sub-packtets
        length = packet.read(LEN_CNT if length_type else LEN_BITS).uint

        while length > 0:  # > 0 to prevent over-reading in bits-mode
            before = packet.pos
            version_, val_ = parse(packet)

            # substract 1 packet cnt if 1, length_type, else substract sub packet length
            length -= 1 if length_type else packet.pos - before  # after - before = consumed length
            version += version_  # sum up versions for part a
            val.append(val_)  # collect values for part b
        assert length == 0  # sanity check

        val = int(OPERATORS[typeid](val))  # apply operator with typeid to values. int to turn bool into int
    return version, val

@level_ab(16, test=False)
def test(line, level):
    # manual tests, as the annotation doesn't allow multiple tests per level with different values
    for h, e in zip(["D2FE28", "38006F45291200", "EE00D40C823060", "8A004A801A8002F478", "620080001611562C8802118E34",
                     "C0015000016115A2E0802F182340", "A0016C880162017C3686B18A3D4780"],
                    [6, 9, 14, 16, 12, 23, 31]):  # version sums
        assert parse(BitStream(hex=h))[0] == e

    for h, e in zip(["C200B40A82", "04005AC33890", "880086C3E88112", "CE00C43D881120", "D8005AC2A8F0", "F600BC2D8F",
                     "9C005AC2F8F0", "9C0141080250320F1802104A08"],
                    [3, 54, 7, 9, 1, 0, 0, 1]):  # expected values
        assert parse(BitStream(hex=h))[1] == e
    return parse(BitStream(hex=line))[level]
