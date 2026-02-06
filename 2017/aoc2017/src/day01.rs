pub fn solve(input: &str, part_b: bool) -> String {
    let mut sum: i32 = 0;
    let chars: Vec<char> = input.chars().collect();
    let len = chars.len();
    for i in 0..len {
        let mut i_other = i;
        i_other += if part_b { len / 2 } else { 1 };
        if chars[i] == chars[i_other % len] {
            sum += chars[i].to_digit(10).unwrap() as i32;
        }
    }
    sum.to_string()
}
