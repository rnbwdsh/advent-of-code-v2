use itertools::Itertools;
use std::collections::HashSet;

pub fn solve(input: &str, _part_b: bool) -> String {
    input
        .split("\n")
        .map(|line| check_line(line, _part_b))
        .sum::<i32>()
        .to_string()
}

fn check_line(line: &str, part_b: bool) -> i32 {
    let mut word_set = HashSet::new();
    for word in line.split_whitespace() {
        let word_fixed = if part_b {
            word.chars().into_iter().sorted().collect()
        } else {
            word.to_string()
        };
        if !word_set.insert(word_fixed) {
            return 0;
        }
    }
    1
}
