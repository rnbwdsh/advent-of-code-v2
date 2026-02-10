use std::collections::HashMap;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
    let mut memory: Vec<u32> = input
        .split_whitespace()
        .map(|x| x.parse())
        .collect::<Result<_, _>>()?;
    let mem_len = memory.len();

    let mut seen: HashMap<Vec<u32>, i32> = HashMap::new();
    seen.insert(memory.clone(), 0);

    for step in 1.. {
        let biggest = *memory.iter().max().ok_or("Empty memory")?;
        let mut biggest_idx = memory.iter().position(|&m| m == biggest).ok_or("Position not found")?;
        memory[biggest_idx] = 0;
        biggest_idx += 1;

        for i in biggest_idx..biggest_idx + biggest as usize {
            memory[i % mem_len] += 1;
        }

        match seen.insert(memory.clone(), step) {
            Some(s) => return Ok((if part_b {step - s} else {step}).to_string()),
            None => continue
        }
    }
    unreachable!()
}
