extern crate core;

macro_rules! aoc_days {
    ($($day:ident),+) => {
        $(mod $day;)+

        fn get_solvers() -> [fn(&str, bool) -> String; count!($($day),+)] {
            [$($day::solve),+]
        }
    };
}

macro_rules! count {
    ($single:tt) => { 1 };
    ($first:tt, $($rest:tt),+) => { 1 + count!($($rest),+) };
}

mod requester;
aoc_days!(day01, day02, day03, day04, day05, day06, day07, day08, day09, day10, day11, day12, day13);

use std::time::Instant;

fn main() {
    let solvers = get_solvers();

    for (solver, day) in solvers.iter().zip(1..) {
        let input = requester::for_level(day as u8);
        for part_b in [false, true] {
            let start = Instant::now();
            println!("day{}{}: {} (took {:?})", day, if part_b { "b" } else { "a" }, solver(&input, part_b), start.elapsed());
        }
    }
}
