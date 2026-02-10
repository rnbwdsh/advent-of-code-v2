use std::error::Error;

fn parse_action_block(action_block: &[&str]) -> Result<(u8, i64, char), Box<dyn Error>> {
    let write_value = action_block[1]
        .split_whitespace()
        .last()
        .ok_or("Invalid write line")?
        .parse()?;

    let move_mod = match action_block[2]
        .split_whitespace()
        .last()
        .ok_or("Invalid move line")?
        .chars()
        .next()
        .ok_or("Invalid move direction")?
    {
        'r' => 1,
        'l' => -1,
        _ => return Err("Invalid move direction".into()),
    };

    let next_state = action_block[3]
        .split_whitespace()
        .last()
        .ok_or("Invalid next state line")?
        .chars()
        .next()
        .ok_or("Invalid next state")?;

    Ok((write_value, move_mod, next_state))
}

pub fn solve(input: &str, _part_b: bool) -> Result<String, Box<dyn Error>> {
    if _part_b {
        return Err("Part B not implemented".into());
    }
    let input_repl = input.replace(".", "");
    let (header, body) = input_repl.split_once("\n\n").ok_or("Invalid input format")?;
    let hdr_parts: Vec<&str> = header.split_whitespace().collect();
    let mut state = hdr_parts[3].chars().next().ok_or("Invalid initial state")?;
    let step_count: usize = hdr_parts[9].parse()?;

    let mut states: Vec<Vec<(u8, i64, char)>> = vec![vec![]; 128];
    for block in body.split("\n\n") {
        let mut lines = block.lines();
        let state_line = lines.next().ok_or("Missing state line")?;
        let state_name = state_line.split_whitespace().nth(2).ok_or("Invalid state line")?.chars().next().ok_or("Invalid state name")?;
        let actions: Result<Vec<_>, _> = lines
            .collect::<Vec<_>>()
            .chunks(4)
            .map(parse_action_block)
            .collect();
        states[state_name as usize] = actions?;
    }

    const OFFSET: usize = 10_000;
    let mut tape = [0u8; OFFSET * 2];
    let mut cursor: i64 = 0;

    for _ in 0..step_count {
        let actions = &states[state as usize];
        let idx = (cursor + OFFSET as i64) as usize;
        let current_value = tape[idx];
        let (write_value, move_direction, next_state) = actions[current_value as usize];
        tape[idx] = write_value;
        cursor += move_direction;
        state = next_state;
    }

    let checksum: usize = tape.iter().filter(|&&v| v == 1).count();
    Ok(checksum.to_string())
}