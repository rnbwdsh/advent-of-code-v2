use crate::common::Generator;

pub fn solve(_input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
    let (l0, l1) = _input.split_once('\n').unwrap();
    let mut a = Generator::new(l0.split_whitespace().last().unwrap().parse()?, 16807);
    let mut b = Generator::new(l1.split_whitespace().last().unwrap().parse()?, 48271);

    let (total, da, db) = if part_b {
        (5_000_000, 4, 8)
    } else {
        (40_000_000, 1, 1)
    };

    Ok((0..total)
        .filter(|_| a.next(da) == b.next(db))
        .count().to_string())
}

