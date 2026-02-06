use itertools::Itertools;
use std::ops::BitXor;

pub fn solve(_input: &str, _part_b: bool) -> String {
    let instructions: Vec<u32> = if _part_b {
        _input.chars().map(|x| x as u32).collect()
    } else {
        _input.split(",").map(|x| x.parse().unwrap()).collect()
    };

    let mut list: Vec<u8> = (0..=255).collect();
    let list_len = list.len();
    let mut rot_total = 0;
    for (skip, instruction) in instructions.iter().enumerate() {
        let mut sublist: Vec<_> = list[0..*instruction as usize].to_vec();
        sublist.reverse();
        list[..sublist.len()].copy_from_slice(&sublist);
        let to_rotate = (*instruction as usize + skip) % list_len;
        rot_total += to_rotate;
        list.rotate_left((*instruction as usize + skip) % list_len);
    }
    list.rotate_right(rot_total % list_len);
    if _part_b {
        let chunk_xor = |block: &[u8]| -> u8 { block.iter().fold(0, u8::bitxor) };
        let dense_hash: Vec<_> = list.chunks(16).map(chunk_xor).collect();
        dense_hash.iter().map(|x| format!("{:02x}", x)).join("")
    } else {
        (list[0] as i32 * list[1] as i32).to_string()
    }
}

