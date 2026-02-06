use reqwest::blocking::Client;
use std::{env, fs, path::PathBuf};

fn with_cache(year: u16, day: u8, read_fn: impl FnOnce(&str) -> String) -> String {
    let home = env::var("HOME")
        .or_else(|_| env::var("USERPROFILE"))
        .expect("Home dir not found");
    let aocd_dir = PathBuf::from(home).join(".config/aocd");

    let binding = fs::read_to_string(aocd_dir.join("token")).expect("Failed to read token file");
    let parts: Vec<&str> = binding.split_whitespace().collect();
    let token = parts.get(0).expect("No token found");
    let username = parts.get(2).expect("No username found");

    let cache_path = aocd_dir
        .join(username)
        .join(format!("{year}_{day:02}_input.txt"));
    if let Ok(cached) = fs::read_to_string(&cache_path) {
        cached
    } else {
        let content = read_fn(token);
        fs::create_dir_all(cache_path.parent().unwrap()).ok();
        fs::write(cache_path, &content).expect("Cache write failed");
        content
    }
}

pub fn for_level(day: u8) -> String {
    let year = 2017;
    with_cache(year, day, |token| {
        Client::new()
            .get(format!("https://adventofcode.com/{year}/day/{day}/input"))
            .header("Cookie", format!("session={token}"))
            .send()
            .expect("Request failed")
            .text()
            .expect("Body failed")
            .trim_end()
            .to_string()
    })
}
