import sys
import math
from queue import PriorityQueue
from collections import defaultdict
import json

import n_puzzle

def manhattan(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                x_solved, y_solved = solved_puzzle_dict[puzzle[y][x]]
                h += abs(x - x_solved) + abs(y - y_solved)
    return h

def euclidian(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                x_solved, y_solved = solved_puzzle_dict[puzzle[y][x]]
                h += math.sqrt((x - x_solved) ** 2 + (y - y_solved) ** 2)
    return h

def hamming(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict):
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

def set_h(heuristic):
    if heuristic == "manhattan"
        return manhatan
    else if heuristic == "euclidian":
        return euclidian
    else if heuristic == "hamming":
        return hamming
    else:
        return boost

def linear_conflict(puzzle, puzzle_size, x, y, solved_puzzle, solved_puzzle_dict):
    x_solved, y solved = solved_puzzle_dict[puzzle[y][x]]
    if puzzle[y_solved][x_solved] == solved_puzzle[y][x] and ((x == x_solved and y_solved > y) or (y == y_solved and x_solved > x)):
        return 2
    return 0

def solve_puzzle(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict, heuristic, search, mute):
    h_func = set_h(heuristic)
    opent_set_queue = PriorityQueue()
    open_set = set()
    closed_set = set()
    closed_set_len = 0
    prev_state = {}
    g = {}
    h = {}
    start_json = json.dumps(puzzle)
    g[start_json] = 0
    h[start_json] = h_func(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict)
    open_set_queue.put((g[start_json] + h[start_json], puzzle))
    open_set.add(start_json)
    open_set_len = 1
    prev_state[start_json] = []
    selected_states = 0
    maximum_states = 0
    while open_set_queue:
        maximum_states = max(open_set_len + closed_set_len, maximum_states)
        f, current_state = open_set_queue.get()
        current_json = json.dumps(current_state)
        open_set.remove(current_json)
        open_set_len -= 1
        selected_states += 1
        if h[current_json] == 0:
            return
        for state in expand():

    return