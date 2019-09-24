import sys
import math

import n_puzzle

def manhattan(puzzle, puzzle_size, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                x_solved, y_solved = solved_puzzle_dict[puzzle[y][x]]
                h += abs(x - x_solved) + abs(y - y_solved)
    return h

def euclidian(puzzle, puzzle_size, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                x_solved, y_solved = solved_puzzle_dict[puzzle[y][x]]
                h += math.sqrt((x - x_solved) ** 2 + (y - y_solved) ** 2)
    return h

def hamming(puzzle, puzzle_size, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                if (x, y) != solved_puzzle_dict[puzzle[y][x]]
                h += 1
    return h

def boost(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                x_solved, y_solved = solved_puzzle_dict[puzzle[y][x]]
                h_curr = abs(x - x_solved) + abs(y - y_solved)
                if h_curr > 0:
                    h += h_curr + linear_conflict(puzzle, puzzle_size, x, y, solved_puzzle, solved_puzzle_dict)
    return h

def linear_conflict(puzzle, puzzle_size, x, y, solved_puzzle, solved_puzzle_dict):
    x_solved, y solved = solved_puzzle_dict[puzzle[y][x]]
    if puzzle[y_solved][x_solved] == solved_puzzle[y][x] and ((x == x_solved and y_solved > y) or (y == y_solved and x_solved > x)):
        return 2
    return 0

def solve_puzzle(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict, heuristic, search, mute):
    return