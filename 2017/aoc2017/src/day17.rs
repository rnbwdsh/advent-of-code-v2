use std::error::Error;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let steps: usize = input.trim().parse()?;
    let mut buffer = vec![0];
    let mut pos = 0;
    if !part_b {
        let iterations = if part_b { 50_000_000 } else { 2017 };
        for i in 1..=iterations {
            pos = (pos + steps) % buffer.len() + 1;
            buffer.insert(pos, i);
        }
        buffer
            .iter()
            .position(|&x| x == 2017)
            .map(|i| buffer[i + 1].to_string())
            .ok_or("Value not found".into())
    } else {
        let mut value_after_zero = 0;
        for i in 1..=50_000_000 {
            pos = (pos + steps) % i + 1;
            if pos == 1 {
                value_after_zero = i;
            }
        }
        Ok(value_after_zero.to_string())
    }
}
