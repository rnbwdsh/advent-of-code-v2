use std::error::Error;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let mut components: Vec<(usize, usize)> = input
        .lines()
        .map(|line| {
            let (a, b) = line.split_once('/').ok_or("Invalid component format")?;
            Ok((a.parse()?, b.parse()?))
        })
        .collect::<Result<_, Box<dyn Error>>>()?;

    let (_length, strength) = replacing_search(&mut components, 0, part_b);
    Ok(strength.to_string())
}

fn replacing_search(components: &mut Vec<(usize, usize)>, port: usize, part_b: bool) -> (usize, usize) {
    let mut max_result = (0, 0);
    for i in (0..components.len()).rev() {
        if components[i].0 == port || components[i].1 == port {
            let next_port = if components[i].0 == port {
                components[i].1
            } else {
                components[i].0
            };
            let strength = components[i].0 + components[i].1;
            let component = components.remove(i);
            let (sub_length, sub_strength) = replacing_search(components, next_port, part_b);
            let current = (sub_length + 1, sub_strength + strength);

            if part_b {
                if current.0 > max_result.0 || (current.0 == max_result.0 && current.1 > max_result.1) {
                    max_result = current;
                }
            } else {
                if current.1 > max_result.1 {
                    max_result = current;
                }
            }

            // replace the component with a contracted version
            components.insert(i, component);
        }
    }
    max_result
}