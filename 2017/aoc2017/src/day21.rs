use std::collections::HashMap;
use std::error::Error;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let mut replacements = HashMap::new();

    for line in input.lines() {
        let (left, right) = line.split_once(" => ").unwrap();
        let mut left = left.replace("/", "");
        let right = right.replace("/", "");

        for _ in 0..2 {
            for _ in 0..4 {
                replacements.entry(left.clone()).or_insert(right.clone());
                left = rotate90(&mut left);
            }
            left = flip(&mut left);
        }
    }

    let mut image: Vec<String> = vec![
        ".#.".to_string(),
        "..#".to_string(),
        "###".to_string(),
    ];

    let repeats = if part_b { 18 } else { 5 };
    for _ in 0..repeats {
        let size = image.len();
        // Determine if we are splitting by 2 or 3
        let (chunk_size, new_chunk_size) = if size % 2 == 0 { (2, 3) } else { (3, 4) };

        let mut new_image: Vec<String> = Vec::new();

        for y in (0..size).step_by(chunk_size) {
            let mut new_rows = vec![String::new(); new_chunk_size];

            for x in (0..size).step_by(chunk_size) {
                let mut key = String::with_capacity(chunk_size * chunk_size);
                for dy in 0..chunk_size {
                    key.push_str(&image[y + dy][x..x + chunk_size]);
                }

                let output = replacements.get(&key).expect("Pattern not found");
                for dy in 0..new_chunk_size {
                    let start = dy * new_chunk_size;
                    let end = start + new_chunk_size;
                    new_rows[dy].push_str(&output[start..end]);
                }
            }
            new_image.extend(new_rows);
        }
        image = new_image;
    }

    let total_on: usize = image.iter()
        .map(|row| row.chars().filter(|&c| c == '#').count())
        .sum();
    Ok(total_on.to_string())
}

fn rotate90(s: &str) -> String {
    let n = (s.len() as f64).sqrt() as usize;
    let chars: Vec<char> = s.chars().collect();
    (0..n * n)
        .map(|i| {
            let (r, c) = (i / n, i % n);
            chars[(n - 1 - c) * n + r]
        })
        .collect()
}

fn flip(s: &str) -> String {
    let n = (s.len() as f64).sqrt() as usize;
    let chars: Vec<char> = s.chars().collect();
    chars.chunks(n)
        .flat_map(|row| row.iter().rev())
        .collect()
}