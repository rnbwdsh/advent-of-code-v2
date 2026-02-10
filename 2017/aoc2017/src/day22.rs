use std::error::Error;
use crate::common::{AreaWithOffset, Point};

const GRID_SIZE: usize = 2048;
const OFFSET: isize = 1024;

#[derive(PartialEq, Copy, Clone)]
enum State {
    Clean,
    Weakened,
    Infected,
    Flagged,
}

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let mut direction = Point::new(0, -1);
    let mut field = AreaWithOffset::new(GRID_SIZE, OFFSET as isize, State::Clean);

    let lines: Vec<&str> = input.lines().collect();
    for (i, line) in lines.iter().enumerate() {
        for (j, c) in line.chars().enumerate() {
            let state = match c {
                '#' => State::Infected,
                '.' => State::Clean,
                _ => {
                    panic!("invalid input")
                }
            };
            let pos = Point::new(j as isize, i as isize);
            field[pos] = state;
        }
    }
    let mut infected_count = 0;
    let height = (lines.len() / 2).try_into()?;
    let width = (lines[0].chars().count() / 2).try_into()?;
    let mut pos = Point::new(width , height);
    let iterations = if part_b { 10000000 } else { 10000 };
    for _ in 0..iterations {
        let infected = field[pos];
        let next_state = if part_b {
            match infected {
                State::Clean => State::Weakened,
                State::Weakened => State::Infected,
                State::Infected => State::Flagged,
                State::Flagged => State::Clean,
            }
        } else {
            match infected {
                State::Clean => State::Infected,
                State::Infected => State::Clean,
                _ => {
                    panic!("invalid state")
                }
            }
        };
        if next_state == State::Infected {
            infected_count += 1;
        }
        field[pos] = next_state;
        let dir_mul = match infected {
            State::Clean => Point::new(0, -1),
            State::Weakened => Point::new(1, 0),
            State::Infected => Point::new(0, 1),
            State::Flagged => Point::new(-1, 0),
        };
        direction *= dir_mul;
        pos += direction;
    }

    Ok(infected_count.to_string())
}
