use num_complex::Complex;
use std::ops::{AddAssign, Index, IndexMut};

// ==== Common Types ====
pub type Point = Complex<isize>;

// ==== Day 3, Day 11, Day 19 - Directions ====
pub const DIRECTIONS: [Point; 4] = [
    Point::new(1, 0),   // Right
    Point::new(-1, 0),  // Left
    Point::new(0, 1),   // Down
    Point::new(0, -1),  // Up
];

// ==== Day 7 - Tree Node ====
pub struct Node {
    pub children: Vec<String>,
    pub weight: i32,
}

// ==== Day 15 - Generator ====
pub struct Generator {
    value: u64,
    factor: u64,
}

impl Generator {
    pub fn new(value: u64, factor: u64) -> Self {
        Self { value, factor }
    }

    pub fn next(&mut self, divisor: u64) -> u64 {
        loop {
            self.value = (self.value * self.factor) % 2147483647;
            if self.value % divisor == 0 {
                return self.value & 0xFFFF;
            }
        }
    }
}

// ==== Day 19 - Area Grid ====
pub struct Area {
    pub grid: Vec<Vec<char>>,
    pub len: isize,
}

impl Area {
    pub fn new(grid: Vec<Vec<char>>) -> Self {
        let len = grid.len() as isize;
        Self { grid, len }
    }

    pub fn in_bounds(&self, pos: Point) -> bool {
        pos.im >= 0 && pos.re >= 0 && pos.im < self.len && pos.re < self.len
    }
}

impl Index<Point> for Area {
    type Output = char;

    fn index(&self, pos: Point) -> &Self::Output {
        &self.grid[pos.im as usize][pos.re as usize]
    }
}

impl IndexMut<Point> for Area {
    fn index_mut(&mut self, pos: Point) -> &mut Self::Output {
        &mut self.grid[pos.im as usize][pos.re as usize]
    }
}

// ==== Day 20 - 3D Point ====
#[derive(Clone, Eq, PartialEq, Hash)]
pub struct P3 {
    pub x: i32,
    pub y: i32,
    pub z: i32,
}

pub struct P3d {
    pub p: P3,
    pub v: P3,
    pub a: P3,
    pub i: usize,
}

impl AddAssign for P3 {
    fn add_assign(&mut self, rhs: Self) {
        self.x += rhs.x;
        self.y += rhs.y;
        self.z += rhs.z;
    }
}

