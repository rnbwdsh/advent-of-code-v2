pub fn solve(input: &str, part_b: bool) -> i32 {
    let mut maze: Vec<i32> = input
        .split_whitespace()
        .map(|x| x.parse().unwrap())
        .collect();

    let mut curr: usize = 0;
    let mut steps: i32 = 0;
    while let Some(offset) = maze.get_mut(curr) {
        let jump = *offset;
        *offset += if part_b && jump >= 3 {-1} else {1};
        steps += 1;
        match curr.checked_add_signed(jump as isize) {
            Some(new_pos) => curr = new_pos,
            None => return steps, 
        }
    }
    steps
}