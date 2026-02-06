use std::collections::HashMap;

pub fn solve(input: &str, part_b: bool) -> String {
    let mut registers = HashMap::new();
    let mut max_overall = 0;

    for line in input.lines() {
        let parts: Vec<&str> = line.split_whitespace().collect();
        let [reg, op, amt, _, cond_reg, cond_op, cond_val] = parts[..] else {
            continue;
        };

        let reg_r_val = *registers.get(cond_reg).unwrap_or(&0);
        let cond_val: i32 = cond_val.parse().unwrap();

        let comparison: fn(&i32, &i32) -> bool = match cond_op {
            "<" => i32::lt,
            ">" => i32::gt,
            "<=" => i32::le,
            ">=" => i32::ge,
            "==" => i32::eq,
            "!=" => i32::ne,
            _ => unreachable!(),
        };

        if comparison(&reg_r_val, &cond_val) {
            let amount: i32 = amt.parse().unwrap();
            let change = if op == "inc" { amount } else { -amount };

            let entry = registers.entry(reg.to_string()).or_insert(0);
            *entry += change;
            max_overall = max_overall.max(*entry);
        }
    }

    (if part_b {
        max_overall
    } else {
        registers.into_values().max().unwrap_or(0)
    }).to_string()
}
