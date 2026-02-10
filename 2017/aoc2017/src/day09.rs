pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
    let mut chars = input.chars();
    let mut depth = 0;
    let mut score = 0;
    let mut garbage_count = 0;
    let mut garbage = false;

    while let Some(ch) = chars.next() {
        match (garbage, ch) {
            (_, '!') => { chars.next(); }
            (false, '<') => garbage = true,
            (true, '>') => garbage = false,
            (false, '{') => depth += 1,
            (false, '}') => {
                score += depth;
                depth -= 1;
            }
            (true, _) => garbage_count += 1,
            _ => {}
        }
    }
    Ok((if part_b { garbage_count } else { score }).to_string())
}
