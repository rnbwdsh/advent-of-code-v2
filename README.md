# All my advent of code solutions so far

## TODO

Fix
* 2019/16
* 2019/18
* 2019/19
* 2019/25
* 2018 -> nim to py
* 2017 -> redo in py
* 2016 -> go to py

## Why

My [previous AoC repo](https://github.com/rnbwdsh/advent-of-code) was a mess, and I wanted to bring everything to a standardized format in python.

To see how my programming skills evolve over time, and to learn pytest

I'd also later like to use this as LLM training data

## How to use

* Install the dependencies mentioned in pyproject.toml
* Run `pytest` in any year-directory. Use -n 32 for parallelism

## Pytest magic + parser

The data is automatically fetched via python pytest fixtures, based on the folder and file name, i.e. for `2025/day_05` 
it will fetch the respective data. Based on the annotated type of the 1st param, i.e. `def test_05(data: np.ndarray, level):`
it will convert the data to a 
* str or int
* List[str] (default) or List[int] (separated by \n)
* List[List[str]] or List[List[int]] (separated by \n\n and \n)
* np.ndarray (2d array of strings)

## Point class

As standard python doesn't have a class for 2d/3d points, I've created a Point class, 
that extends Tuple with +, -, *, //, abs (sum of abs coords) and dist (euclidean).

It also supports 2d-neighbors and opposite directions, and a PointList for calculating the area, as well as L, R, U, D constants + a DIR list.