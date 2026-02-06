use itertools::iproduct;
use num_complex::Complex;
use std::collections::HashMap;

type Point = Complex<i32>;
type Grid = HashMap<Point, i32>;

pub fn solve(input: &str, part_b: bool) -> i32 {
    let end = input.parse().expect("input was no int");

    let mut grid: Grid = HashMap::new();
    if part_b {
        grid.insert(Point::new(0, 0), 1);
        grid.insert(Point::new(1, 0), 1);
    }

    let mut dir: Point = Point::new(0, 1);
    let mut pos = Point::new(1, 0);
    let mut turn_next = false;

    for step in 3.. {
        if turn_next {
            dir *= Complex::i();
            turn_next = false;
        } else if pos.re.abs() == pos.im.abs() {
            if pos.re > 0 && pos.im < 0 {
                turn_next = true
            } else {
                dir *= Complex::i();
            }
        }
        pos += dir;
        if part_b {
            let next = set_next_neighbor(&mut grid, pos);
            if next > end {
                return next;
            }
        } else if step == end {
            return pos.re.abs() + pos.im.abs();
        }
    }
    unreachable!()
}

fn set_next_neighbor(map: &mut Grid, p: Point) -> i32 {
    let sum: i32 = iproduct!(-1..=1, -1..=1)
        .map(|(dx, dy)| p + Complex::new(dx, dy))
        .filter_map(|neighbor| map.get(&neighbor).copied())
        .sum();
    *map.entry(p).or_insert(sum)
}
