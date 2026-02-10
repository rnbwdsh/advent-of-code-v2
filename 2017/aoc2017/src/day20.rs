use crate::common::{P3, P3d};
use std::collections::{HashMap, HashSet};
use std::error::Error;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let mut particles: Vec<P3d> = input.lines().enumerate()
        .map(|(i, line)| parse_particle(i, line))
        .collect::<Result<Vec<_>, Box<dyn Error>>>()?;
    for _ in 0..1000 {
        for p in &mut particles {
            p.v += p.a.clone();
            p.p += p.v.clone();
        }
        if part_b {
            let mut positions = HashMap::new();
            let mut to_remove = HashSet::new();
            for p in particles.iter() {
                if let Some(prev) = positions.insert(&p.p, p.i) {
                    to_remove.insert(p.i);
                    to_remove.insert(prev);
                }
            }
            particles.retain(|p| !to_remove.contains(&p.i));
        }
    }

    Ok(if part_b {
        particles.len()
    } else {
        find_smallest_idx(&particles)
    }.to_string())
}

fn find_smallest_idx(particles: &[P3d]) -> usize {
    particles.iter()
        .min_by_key(|p| manhattan_distance(&p.p))
        .map(|p| p.i)
        .unwrap_or(0)
}

fn parse_particle(i: usize, line: &str) -> Result<P3d, Box<dyn Error>> {
    let mut parts = line.split(", ");
    Ok(P3d {
        p: parse_vector(parts.next().ok_or("missing p")?)?,
        v: parse_vector(parts.next().ok_or("missing v")?)?,
        a: parse_vector(parts.next().ok_or("missing a")?)?,
        i
    })
}

fn parse_vector(s: &str) -> Result<P3, Box<dyn Error>> {
    let coords = s.split('<').nth(1).ok_or("missing <")?.trim_end_matches('>');
    let mut nums = coords.split(',').map(|n| n.parse::<i32>());
    Ok(P3 {
        x: nums.next().ok_or("missing x")??,
        y: nums.next().ok_or("missing y")??,
        z: nums.next().ok_or("missing z")??,
    })
}

fn manhattan_distance(p: &P3) -> usize {
    (p.x.abs() + p.y.abs() + p.z.abs()) as usize
}