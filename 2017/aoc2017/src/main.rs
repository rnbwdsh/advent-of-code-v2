mod requester;
mod day01;
mod day02;
mod day03;
mod day04;
mod day05;
mod day06;
mod day07;
mod day08;
mod day09;
mod day10;

fn main() {
    let solvers = [day01::solve, day02::solve, day03::solve, day04::solve, day05::solve, day06::solve, day07::solve, day08::solve, day09::solve, day10::solve];
    for (solver, day) in solvers.iter().zip(1..) {
        let input = requester::for_level(day as u8);
        for part_b in [false, true] {
            let solution = solver(&input, part_b);
            println!("day{}{}: {}", day, if part_b { "b" } else { "a" }, solution);
        }
    }
}

