pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
    let layers: Vec<(usize, i32)> = input
        .lines()
        .filter_map(|line| {
            let (layer, depth) = line.split_once(": ")?;
            Some((layer.parse().ok()?, depth.parse().ok()?))
        })
        .collect();

    if part_b {
        Ok(calculate_offset(&layers).to_string())
    } else {
        Ok(calculate_score(&layers, 0).to_string())
    }
}

fn calculate_offset(layers: &[(usize, i32)]) -> i64 {
    (0..).find(|&offset| calculate_score(layers, offset) == 0).unwrap()
}

fn calculate_score(layers: &[(usize, i32)], offset: i64) -> i32 {
    let mut score = 0;
    for &(layer_idx, depth) in layers {
        let period = 2 * (depth - 1) as i64;
        if (layer_idx as i64 + offset) % period == 0 {
            if offset != 0 {
                return 1;
            }
            score += layer_idx as i32 * depth;
        }
    }
    score
}
