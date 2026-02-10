use std::collections::HashMap;
use std::error::Error;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let mut prog: Vec<char> = "abcdefghijklmnop".chars().collect();
    let mut seen: HashMap<String, usize> = HashMap::new();
    let repetitions = if part_b { 1_000_000_000 } else { 1 };
    for curr in 0..repetitions {
        forward_program(input, &mut prog)?;
        let prog_str: String = prog.iter().collect();
        if part_b {
            if let Some(&prev) = seen.get(&prog_str) {
                let cycle_len = curr - prev;
                for _ in 0..(repetitions - curr - 1) % cycle_len {
                    forward_program(input, &mut prog)?;
                }
                break;
            } else {
                seen.insert(prog_str, curr);
            }
        } else {
            break;
        }
    }
    Ok(prog.iter().collect())
}

fn forward_program(input: &str, prog: &mut Vec<char>) -> Result<(), Box<dyn Error>> {
    let len = prog.len();
    for c in input.split(",") {
        match c.chars().next() {
            Some('s') => {
                let n: usize = c[1..].parse()?;
                prog.rotate_right(n % len);
            }
            Some('x') => {
                let (a, b) = c[1..].split_once("/").ok_or("Invalid command")?;
                prog.swap(a.parse()?, b.parse()?);
            }
            Some('p') => {
                let (a, b) = c[1..].split_once("/").ok_or("Invalid command")?;
                let pos_a = prog
                    .iter()
                    .position(|&x| x == a.chars().next().unwrap())
                    .unwrap();
                let pos_b = prog
                    .iter()
                    .position(|&x| x == b.chars().next().unwrap())
                    .unwrap();
                prog.swap(pos_a, pos_b);
            }
            _ => return Err("Invalid command".into()),
        }
    }
    Ok(())
}
