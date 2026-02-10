use crate::day18::Program;
use std::collections::VecDeque;
use std::error::Error;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let mut code = Vec::new();
    for line in input.lines() {
        let mut line_iter = line.split_whitespace().into_iter();
        code.push((
            line_iter.next().ok_or("Empty line")?.to_string(),
            line_iter.next().ok_or("Missing argument")?.to_string(),
            line_iter.next().map(|s| s.to_string()),
        ));
    }

    if !part_b {
        let mut prog0 = Program::new(code.clone(), 0);
        // run the program and return the mul count
        let mut inbox = VecDeque::new();
        while prog0.step(&mut inbox) {}
        Ok(prog0.mul_count.to_string())
    } else {
        let cnt = (109300..=126300)
            .step_by(17)
            .filter(|&d| {
                let limit = (d as f64).sqrt() as i64;
                (2..=limit).any(|i| d % i == 0)
            })
            .count();
        Ok(cnt.to_string())
    }
}
