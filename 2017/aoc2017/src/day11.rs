use std::cmp::max;

pub fn solve(input: &str, part_b: bool) -> String {
    let (mut x, mut y, mut z): (i32, i32, i32) = (0, 0, 0);
    let mut max_dist = 0;

    for dir in input.trim().split(",") {
        match dir {
            "n" => {
                y += 1;
                z -= 1;
            }
            "s" => {
                y -= 1;
                z += 1;
            }
            "ne" => {
                x += 1;
                z -= 1;
            }
            "sw" => {
                x -= 1;
                z += 1;
            }
            "nw" => {
                x -= 1;
                y += 1;
            }
            "se" => {
                x += 1;
                y -= 1;
            }
            _ => panic!("Unknown direction"),
        }

        if part_b {
            max_dist = max(max_dist, (x.abs() + y.abs() + z.abs()) / 2);
        }
    }

    if part_b {
        max_dist
    } else {
        (x.abs() + y.abs() + z.abs()) / 2
    }
    .to_string()
}
