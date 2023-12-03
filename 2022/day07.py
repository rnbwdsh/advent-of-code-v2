from typing import Dict

def dir_sum(dir_name: str, root: Dict[str, Dict], dirs_name_size: Dict[str, int]) -> int:
    """ recursively sum up sizes of subdirectories and add all to a global list """
    total_size = 0
    for file_name, file_dict_or_size in root.items():
        if type(file_dict_or_size) == dict and file_name != "..":
            total_size += dir_sum(dir_name + "/" + file_name, file_dict_or_size, dirs_name_size)
        elif type(file_dict_or_size) == int:
            total_size += file_dict_or_size
    dirs_name_size[dir_name] = total_size
    return total_size

def test_07(data, level):
    root = curr = dict()
    for line in data:
        a, b, *c = line.split(" ")
        if a == "$":
            if b == "cd":  # just ignore ls case
                c = c[0]
                curr = root if c == "/" else curr[c]
        else:
            curr[b] = {"..": curr} if a == "dir" else int(a)
    total = dir_sum("", root, dirs_name_size := dict())
    level_filter = [lambda s: s < 100_000, lambda s: s > total - 40000000][level]
    sizes = sorted(filter(level_filter, dirs_name_size.values()))
    return min(sizes) if level else sum(sizes)
