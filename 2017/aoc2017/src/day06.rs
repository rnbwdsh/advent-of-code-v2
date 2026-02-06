use std::collections::HashMap;

pub fn solve(input: &str, part_b: bool) -> i32 {
    let mut memory: Vec<u32> = input
        .split_whitespace()
        .map(|x| x.parse().expect("non-u32 compatible value found"))
        .collect();
    let mem_len = memory.len();

    let mut seen: HashMap<Vec<u32>, i32> = HashMap::new();
    seen.insert(memory.clone(), 0);

    for step in 1.. {
        let biggest = *memory.iter().max().unwrap();
        let mut biggest_idx = memory.iter().position(|&m| m == biggest).unwrap();
        memory[biggest_idx] = 0;
        biggest_idx += 1;

        for i in biggest_idx..biggest_idx + biggest as usize {
            memory[i % mem_len] += 1;
        }

        match seen.insert(memory.clone(), step) {
            Some(s) => return if part_b {step - s} else {step},
            None => continue
        }
    }
    unreachable!()
}
