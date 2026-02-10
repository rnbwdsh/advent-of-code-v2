use crate::common::{AreaWithOffset, Point};
use itertools::Itertools;
use std::error::Error;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let grid = input.lines().map(|line| line.chars().collect::<Vec<char>>()).collect::<Vec<Vec<char>>>();
    let size = grid.len();
    let mut area = AreaWithOffset {
        grid: grid.clone(),
        size,
        offset: 0,
    };
    let curr_x = grid[0].iter().enumerate().filter(|(_i, p)| **p == '|').next().unwrap().0;
    let mut letters: Vec<char> = Vec::new();
    let mut curr_pos = Point::new(curr_x as isize, 0);
    let mut direction = Point::new(0, 1);
    let mut step_letter = 0;
    let mut step = 1;
    loop {
        step += 1;
        area[curr_pos] = ' ';
        curr_pos = curr_pos + direction;

        if !area.in_bounds(curr_pos) {
            break;
        }
        if area[curr_pos] == '+' {
            for d2 in [
                Point::new(1, 0),   // Right
                Point::new(-1, 0),  // Left
                Point::new(0, 1),   // Down
                Point::new(0, -1),  // Up
            ] {
                let p2 = curr_pos + d2;
                if area.in_bounds(p2) && area[p2] != ' ' {
                    direction = d2;
                    break;
                }
            }
        } else if area[curr_pos].is_alphabetic() {
            letters.push(area[curr_pos]);
            step_letter = step;
        }
    }

    if part_b { Ok(step_letter.to_string()) } else { Ok(letters.iter().join("")) }
}