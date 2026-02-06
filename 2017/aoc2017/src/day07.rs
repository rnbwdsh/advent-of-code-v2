use std::collections::{HashMap, HashSet};
use itertools::Itertools;

struct Node {
    children: Vec<String>,
    weight: i32,
}
pub fn solve(input: &str, part_b: bool) -> i32 {
    let mut tree: HashMap<String, Node> = HashMap::new();

    for line in input.lines() {
        let (left, right) = line.split_once(" -> ").unwrap_or((line, ""));

        let mut left_parts = left.split_whitespace();
        let name = left_parts.next().unwrap();
        let weight: i32 = left_parts
            .next()
            .unwrap()
            .trim_matches(|c| c == '(' || c == ')')
            .parse()
            .unwrap();

        let children: Vec<String> = if right.is_empty() {
            Vec::new()
        } else {
            right.split(", ").map(String::from).collect()
        };

        tree.insert(name.to_string(), Node{children, weight});
    }

    let all_nodes: HashSet<_> = tree.keys().collect();
    let all_children: HashSet<_> = tree.values().flat_map(|node| &node.children).collect();
    let root = all_nodes.difference(&all_children).next().unwrap();

    if !part_b {
        println!("{}", root);
        return 0;
    }

    check_tree(root, &tree).expect("no imbalance found")
}

fn check_tree(curr: &String, tree: &HashMap<String, Node>) -> Option<i32> {
    let curr_children= &tree.get(curr).unwrap().children;
    if curr_children.len() < 2 {
        return None;
    }
    let weights: Vec<i32> = curr_children.iter().map(|c| get_weight(c, tree)).collect();
    let majority_weight = *weights.iter().duplicates().next().unwrap();
    curr_children
        .iter()
        .zip(&weights)
        .find(|(_, w)| **w != majority_weight)
        .and_then(|(child, &w)| {
            check_tree(child, tree).or_else(|| Some(tree[child].weight + (majority_weight - w)))
        })
}

fn get_weight(p0: &String, p1: &HashMap<String, Node>) -> i32 {
    let node = p1.get(p0).unwrap();
    node.weight + node.children.iter().map(|c| get_weight(c, p1)).sum::<i32>()
}
