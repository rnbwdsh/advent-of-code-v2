use itertools::iproduct;

pub fn solve(input: &str, part_b: bool) -> i32 {
    let mut sum = 0;
    for line in input.split("\n") {
        let nums: Vec<i32> = line
            .split_whitespace()
            .map(move |x| x.parse().unwrap())
            .collect();
        if !part_b {
            sum += nums.iter().max().unwrap() - nums.iter().min().unwrap();
        } else {
            sum += check_nums(&nums)
        }
    }
    sum
}

fn check_nums(nums: &[i32]) -> i32 {
    iproduct!(nums, nums)
        .find(|&(curr, other)| curr != other && other % curr == 0)
        .map(|(curr, other)| other / curr)
        .unwrap_or(0)
}
