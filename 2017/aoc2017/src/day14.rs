use std::sync::mpsc;
use std::thread;

type RowResult = Result<(usize, [u8; 128], usize), String>;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
    let (tx, rx) = mpsc::channel();
    let handles: Vec<_> = (0..128)
        .map(|row_id| {
            let tx = tx.clone();
            let input = input.to_string();
            thread::spawn(move || {
                tx.send(calculate_row(row_id, &input)).ok();
            })
        })
        .collect();
    drop(tx);

    let mut area = [[0u8; 128]; 128];
    let mut total_used_squares = 0;

    for result in rx {
        let (row_id, row_data, used_squares) = result?;
        area[row_id] = row_data;
        total_used_squares += used_squares;
    }

    for handle in handles {
        handle.join().unwrap();
    }

    if part_b {
        Ok((0..128)
            .flat_map(|i| (0..128).map(move |j| mark_region(&mut area, i, j)))
            .sum::<usize>()
            .to_string())
    } else {
        Ok(total_used_squares.to_string())
    }
}

fn mark_region(grid: &mut [[u8; 128]; 128], r: usize, c: usize) -> usize {
    let Some(row) = grid.get_mut(r) else { return 0 };
    let Some(cell) = row.get_mut(c) else { return 0 };
    if *cell == 0 {
        return 0;
    }
    *cell = 0;

    [(r.wrapping_sub(1), c), (r + 1, c), (r, c.wrapping_sub(1)), (r, c + 1)]
        .iter()
        .for_each(|&(nr, nc)| {
            mark_region(grid, nr, nc);
        });

    1
}

fn calculate_row(row_id: usize, input: &str) -> RowResult {
    let knot_hash_input = format!("{}-{}", input, row_id);
    let knot_hash = super::day10::solve(&knot_hash_input, true)
        .map_err(|e| format!("Knot hash failed: {}", e))?;

    let mut row_data = [0u8; 128];
    let mut used_squares = 0;

    for (i, hex_char) in knot_hash.chars().enumerate() {
        let byte_value = hex_char
            .to_digit(16)
            .ok_or_else(|| "Invalid hex character".to_string())? as u8;
        for bit in 0..4 {
            let val = (byte_value >> (3 - bit)) & 1;
            row_data[i * 4 + bit] = val;
            used_squares += val as usize;
        }
    }

    Ok((row_id, row_data, used_squares))
}
