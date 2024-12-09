from typing import List

import numpy as np

def parse_chunks_int(data: str) -> List[List[int]]:
    return [parse_line_int(line) for line in data.split("\n\n")]

def parse_line_int(data: str) -> List[int]:
    split_chars = set(data) - set("-0123456789")
    split_char = list(split_chars)[0] if split_chars else "\n"
    return [int(i) for i in data.split(split_char)]

def parse_line(data: str) -> List[str]:
    return data.split("\n\n" if "\n\n" in data else "\n")

def parse_chunks(data: str) -> List[List[str]]:
    return [parse_line(line) for line in data.split("\n\n")]

def parse_array(data: str) -> np.ndarray:
    return np.array([list(line) for line in data.split("\n")])

TYPE_PARSER = {
    List[List[int]]: parse_chunks_int,
    List[List[str]]: parse_chunks,
    List[int]: parse_line_int,
    List[str]: parse_line,
    str: lambda d: d,
    None: lambda d: d.split("\n"),
    np.ndarray: parse_array,
    np.array: parse_array,
    int: int,
}