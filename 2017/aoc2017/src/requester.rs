use reqwest::blocking::Client;
use std::{env, fs, path::PathBuf};

fn with_cache(
    year: u16,
    day: u8,
    read_fn: impl FnOnce(&str) -> Result<String, Box<dyn std::error::Error>>,
) -> Result<String, Box<dyn std::error::Error>> {
    let home = env::var("HOME").or_else(|_| env::var("USERPROFILE"))?;
    let aocd_dir = PathBuf::from(home).join(".config/aocd");

    let binding = fs::read_to_string(aocd_dir.join("token"))?;
    let parts: Vec<&str> = binding.split_whitespace().collect();
    let token = parts.get(0).ok_or("No token found")?;
    let username = parts.get(2).ok_or("No username found")?;

    let cache_path = aocd_dir
        .join(username)
        .join(format!("{year}_{day:02}_input.txt"));
    if let Ok(cached) = fs::read_to_string(&cache_path) {
        Ok(cached)
    } else {
        let content = read_fn(token)?;
        fs::create_dir_all(cache_path.parent().ok_or("Invalid cache path")?)?;
        fs::write(cache_path, &content)?;
        Ok(content)
    }
}

pub fn for_level(day: u8) -> Result<String, Box<dyn std::error::Error>> {
    let year = 2017;
    with_cache(year, day, |token| {
        let response = Client::new()
            .get(format!("https://adventofcode.com/{year}/day/{day}/input"))
            .header("Cookie", format!("session={token}"))
            .send()?
            .text()?;
        Ok(response[..response.len()-1].to_string())
    })
}
