use std::cmp::max;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
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
            _ => return Err("Unknown direction".into()),
        }

        if part_b {
            max_dist = max(max_dist, (x.abs() + y.abs() + z.abs()) / 2);
        }
    }

    Ok((if part_b {
        max_dist
    } else {
        (x.abs() + y.abs() + z.abs()) / 2
    })
    .to_string())
}
