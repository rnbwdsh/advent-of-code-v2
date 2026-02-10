use core::array::from_fn;
use itertools::Itertools;
use std::ops::BitXor;

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
    let suffix = [17, 31, 73, 47, 23] as [u8; _];
    let instructions: Vec<u8> = if part_b {
        input.chars().map(|x| x as _).chain(suffix.iter().copied()).collect()
    } else {
        input.split(",").map(|x| x.parse()).collect::<Result<_, _>>()?
    };

    let nr_rounds = if part_b { 64 } else { 1 };
    let instructions: Vec<u8> = instructions.iter().cycle().take(instructions.len() * nr_rounds).cloned().collect();

    let mut buf: [u8; 256] = from_fn(|i| i as u8);
    let list_len = buf.len();
    let mut rot_total = 0;
    for (skip, instruction) in instructions.iter().enumerate() {
        let mut sublist: Vec<_> = buf[0..*instruction as usize].to_vec();
        sublist.reverse();
        buf[..sublist.len()].copy_from_slice(&sublist);
        let to_rotate = (*instruction as usize + skip) % list_len;
        rot_total += to_rotate;
        buf.rotate_left((*instruction as usize + skip) % list_len);
    }
    buf.rotate_right(rot_total % list_len);
    Ok(if part_b {
        let chunk_xor = |block: &[u8]| -> u8 { block.iter().fold(0, u8::bitxor) };
        let dense_hash: Vec<_> = buf.chunks(16).map(chunk_xor).collect();
        dense_hash.iter().map(|x| format!("{:02x}", x)).join("")
    } else {
        (buf[0] as i32 * buf[1] as i32).to_string()
    })
}

