use itertools::iproduct;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
    let mut sum = 0;
    for line in input.split("\n") {
        let nums: Vec<i32> = line
            .split_whitespace()
            .map(|x| x.parse())
            .collect::<Result<_, _>>()?;
        if !part_b {
            sum += nums.iter().max().ok_or("Empty line")? - nums.iter().min().ok_or("Empty line")?;
        } else {
            sum += check_nums(&nums)
        }
    }
    Ok(sum.to_string())
}

fn check_nums(nums: &[i32]) -> i32 {
    iproduct!(nums, nums)
        .find(|&(curr, other)| curr != other && other % curr == 0)
        .map(|(curr, other)| other / curr)
        .unwrap_or(0)
}
