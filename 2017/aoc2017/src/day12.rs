use std::collections::{HashMap, HashSet};

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn std::error::Error>> {
    let graph: HashMap<i32, Vec<i32>> = input
        .lines()
        .filter_map(|line| {
            let (node, neighbors_str) = line.split_once(" <-> ")?;
            let node_id = node.parse().ok()?;
            let neighbors = neighbors_str
                .split(", ")
                .filter_map(|s| s.parse().ok())
                .collect();
            Some((node_id, neighbors))
        })
        .collect();

    if part_b {
        Ok(count_groups(&graph).to_string())
    } else {
        Ok(visit_group(&graph, 0).len().to_string())
    }
}

fn count_groups(graph: &HashMap<i32, Vec<i32>>) -> usize {
    let mut unseen: HashSet<i32> = graph.keys().copied().collect();
    let mut count = 0;
    while let Some(&node) = unseen.iter().next() {
        let group = visit_group(graph, node);
        unseen.retain(|n| !group.contains(n));
        count += 1;
    }
    count
}

fn visit_group(graph: &HashMap<i32, Vec<i32>>, start: i32) -> HashSet<i32> {
    let mut seen = HashSet::new();
    let mut to_visit = vec![start];
    while let Some(curr) = to_visit.pop() {
        if seen.insert(curr) {
            if let Some(neighbors) = graph.get(&curr) {
                to_visit.extend(neighbors);
            }
        }
    }
    seen
}
