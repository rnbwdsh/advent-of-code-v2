use std::collections::{HashMap, VecDeque};
use std::error::Error;

pub struct Program {
    pub reg: HashMap<String, i64>,
    pub prog: Vec<(String, String, Option<String>)>,
    pub inbox: VecDeque<i64>,
    pub send_count: usize,
    pub pc: usize,
}

impl Program {
    pub fn new(prog: Vec<(String, String, Option<String>)>, pid: i64) -> Self {
        let mut reg: HashMap<String, i64> =
            prog.iter().map(|(_, arg1, _)| (arg1.clone(), 0)).collect();
        reg.insert("p".to_string(), pid);
        Program {
            reg,
            prog,
            inbox: VecDeque::new(),
            send_count: 0,
            pc: 0,
        }
    }

    pub fn get_value(&self, arg: &str) -> i64 {
        arg.parse()
            .ok()
            .unwrap_or_else(|| self.reg.get(arg).cloned().unwrap_or(0))
    }

    pub fn step(&mut self, outbox: &mut VecDeque<i64>) -> bool {
        if self.pc >= self.prog.len() {
            return false;
        }

        let (cmd, arg1, arg2) = &self.prog[self.pc].clone();

        let val1 = self.get_value(&arg1);
        let val2 = arg2.as_ref().map(|s| self.get_value(s)).unwrap_or(0);

        match cmd.as_str() {
            "snd" => {
                outbox.push_back(val1);
                self.send_count += 1;
            }
            "set" | "add" | "mul" | "mod" => {
                self.reg.insert(
                    arg1.clone(),
                    match cmd.as_str() {
                        "set" => val2,
                        "add" => val1 + val2,
                        "mul" => val1 * val2,
                        "mod" => val1 % val2,
                        _ => unreachable!(),
                    },
                );
            }
            "rcv" => {
                if let Some(val) = self.inbox.pop_front() {
                    self.reg.insert(arg1.clone(), val);
                } else {
                    return false;
                }
            }
            "jgz" => {
                if val1 > 0 {
                    self.pc = (self.pc as i64 + val2) as usize;
                    return true;
                }
            }
            _ => {}
        }
        self.pc += 1;
        true
    }
}

pub fn solve(input: &str, part_b: bool) -> Result<String, Box<dyn Error>> {
    let mut prog = Vec::new();
    for line in input.lines() {
        let mut line_iter = line.split_whitespace().into_iter();
        prog.push((
            line_iter.next().ok_or("Empty line")?.to_string(),
            line_iter.next().ok_or("Missing argument")?.to_string(),
            line_iter.next().map(|s| s.to_string()),
        ));
    }

    let mut prog0 = Program::new(prog.clone(), 0);
    if part_b {
        let mut prog1 = Program::new(prog, 1);
        loop {
            let running0 = prog0.step(&mut prog1.inbox);
            let running1 = prog1.step(&mut prog0.inbox);
            if !running0 && !running1 {
                return Ok(prog1.send_count.to_string());
            }
        }
    } else {
        let mut outbox = VecDeque::new();
        while prog0.step(&mut outbox) {}
        Ok(outbox.back().unwrap().to_string())
    }
}
