use num_complex::Complex;
use std::ops::{AddAssign, Index, IndexMut};

// ==== Common Types ====
pub type Point = Complex<isize>;

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

// ==== Day 19 & Day 22 - Generic Area Grid with Offset Support ====
pub struct AreaWithOffset<T> {
    pub grid: Vec<Vec<T>>,
    pub size: usize,
    pub offset: isize,
}

impl<T: Clone> AreaWithOffset<T> {
    pub fn new(size: usize, offset: isize, default: T) -> Self {
        Self {
            grid: vec![vec![default; size]; size],
            size,
            offset,
        }
    }

    pub fn in_bounds(&self, pos: Point) -> bool {
        let x = pos.re + self.offset;
        let y = pos.im + self.offset;
        x >= 0 && y >= 0 && x < self.size as isize && y < self.size as isize
    }
}

impl<T> Index<Point> for AreaWithOffset<T> {
    type Output = T;

    fn index(&self, pos: Point) -> &Self::Output {
        let x = (pos.re + self.offset) as usize;
        let y = (pos.im + self.offset) as usize;
        &self.grid[y][x]
    }
}

impl<T> IndexMut<Point> for AreaWithOffset<T> {
    fn index_mut(&mut self, pos: Point) -> &mut Self::Output {
        let x = (pos.re + self.offset) as usize;
        let y = (pos.im + self.offset) as usize;
        &mut self.grid[y][x]
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

