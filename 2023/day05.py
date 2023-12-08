from typing import List, Optional

import pytest


@pytest.mark.data("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""", 35, 46)
def test_05(data: List[List[str]], level):
    seeds = [int(i) for i in data[0][0].split(": ")[1].split(" ")]
    if level:
        seeds = [range(a, a+b) for a, b in zip(seeds[::2], seeds[1::2])]
    else:
        seeds = [range(s, s+1) for s in seeds]
    for chunk in data[1:]:
        mapper = {}
        for line in chunk[1:]:
            dst, src, ran = [int(i) for i in line.split(" ")]
            mapper[range(src, src+ran)] = range(dst, dst+ran)
        seeds = map_ranges(seeds, mapper)
    return min([s.start for s in seeds])


def range_(start: int, stop: int) -> Optional[range]:
    if start >= stop:
        return None
    return range(start, stop)

def range_intersection(seed: range, to_match: range) -> (Optional[range], Optional[range], Optional[range]):
    start = max(seed.start, to_match.start)
    stop = min(seed.stop, to_match.stop)
    return range_(start, stop)

def map_ranges(seeds, range_mapping):
    mapped_ranges = set()
    while seeds:
        seed_range = seeds.pop()
        if seed_range is None:
            continue
        for src_range, target_range in range_mapping.items():
            intersect = range_intersection(seed_range, src_range)
            if intersect:
                length = intersect.start - src_range.start
                start = target_range.start + length
                mapped_range = range_(start, start + len(intersect))
                mapped_ranges.add(mapped_range)
                seeds.append(range_(seed_range.start, intersect.start))
                seeds.append(range_(intersect.stop, seed_range.stop))
                break
        else:
            mapped_ranges.add(seed_range)
    return list(mapped_ranges)
