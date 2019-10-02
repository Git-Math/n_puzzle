import sys
import math
from queue import PriorityQueue
from collections import defaultdict
import json

import n_puzzle

def heuristic_prev_empty(x, y, prev_direction):
    if prev_direction == "l":
        prev_x = x + 1
        prev_y = y
    elif prev_direction == "r":
        prev_x = x - 1
        prev_y = y
    elif prev_direction == "u":
        prev_x = x
        prev_y = y + 1
    elif prev_direction == "d":
        prev_x = x
        prev_y = y - 1
    return prev_x, prev_y

def manhattan(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                x_solved, y_solved = solved_puzzle_dict[puzzle[y][x]]
                h += abs(x - x_solved) + abs(y - y_solved)
    return h

def manhattan_update(puzzle, solved_puzzle, solved_puzzle_dict, prev_h, prev_direction):
    x, y = n_puzzle.find_empty_square(puzzle)
    prev_x, prev_y = heuristic_prev_empty(x, y, prev_direction)
    x_solved, y_solved = solved_puzzle_dict[puzzle[prev_y][prev_x]]
    return prev_h + abs(prev_x - x_solved) + abs(prev_y - y_solved) - (abs(x - x_solved) + abs(y - y_solved))

def euclidian(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                x_solved, y_solved = solved_puzzle_dict[puzzle[y][x]]
                h += math.sqrt((x - x_solved) ** 2 + (y - y_solved) ** 2)
    return h

def euclidian_update(puzzle, solved_puzzle, solved_puzzle_dict, prev_h, prev_direction):
    x, y = n_puzzle.find_empty_square(puzzle)
    prev_x, prev_y = heuristic_prev_empty(x, y, prev_direction)
    x_solved, y_solved = solved_puzzle_dict[puzzle[prev_y][prev_x]]
    return prev_h + math.sqrt((prev_x - x_solved) ** 2 + (prev_y - y_solved) ** 2) - (math.sqrt((x - x_solved) ** 2 + (y - y_solved) ** 2))

def hamming(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict):
    h = 0
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != 0:
                if (x, y) != solved_puzzle_dict[puzzle[y][x]]:
                    h += 1
    return h

def hamming_update(puzzle, solved_puzzle, solved_puzzle_dict, prev_h, prev_direction):
    x, y = n_puzzle.find_empty_square(puzzle)
    prev_x, prev_y = heuristic_prev_empty(x, y, prev_direction)
    x_solved, y_solved = solved_puzzle_dict[puzzle[prev_y][prev_x]]
    return prev_h + (1 if (prev_x, prev_y) != solved_puzzle_dict[puzzle[prev_y][prev_x]] else 0)  - (1 if (x, y) != solved_puzzle_dict[puzzle[prev_y][prev_x]] else 0)

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
    if heuristic == "manhattan":
        return manhattan, manhattan_update
    elif heuristic == "euclidian":
        return euclidian, euclidian_update
    elif heuristic == "hamming":
        return hamming, hamming_update
    else:
        return boost, manhattan_update

def linear_conflict(puzzle, puzzle_size, x, y, solved_puzzle, solved_puzzle_dict):
    x_solved, y_solved = solved_puzzle_dict[puzzle[y][x]]
    if puzzle[y_solved][x_solved] == solved_puzzle[y][x] and ((x == x_solved and y_solved > y) or (y == y_solved and x_solved > x)):
        return 2
    return 0

def deepcopy(puzzle):
    puzzle_copy = []
    for row in puzzle:
        puzzle_copy.append(list(row))
    return puzzle_copy

def expand(puzzle, puzzle_size, prev_direction):
    x, y = n_puzzle.find_empty_square(puzzle)
    states = []
    if x - 1 >= 0 and prev_direction != "r":
        state = deepcopy(puzzle)
        state[y][x] = state[y][x - 1]
        state[y][x - 1] = 0
        states.append((state, "l"))
    if x + 1 < puzzle_size and prev_direction != "l":
        state = deepcopy(puzzle)
        state[y][x] = state[y][x + 1]
        state[y][x + 1] = 0
        states.append((state, "r"))
    if y - 1 >= 0 and prev_direction != "d":
        state = deepcopy(puzzle)
        state[y][x] = state[y - 1][x]
        state[y - 1][x] = 0
        states.append((state, "u"))
    if y + 1 < puzzle_size and prev_direction != "u":
        state = deepcopy(puzzle)
        state[y][x] = state[y + 1][x]
        state[y + 1][x] = 0
        states.append((state, "d"))
    return states

def solve_puzzle(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict, heuristic, search):
    h_func, h_update_func = set_h(heuristic)
    opened_set_queue = PriorityQueue()
    opened_set = set()
    closed_set = set()
    closed_set_len = 0
    prev_state = {}
    prev_direction = {}
    g = {}
    h = {}
    start_json = json.dumps(puzzle)
    g[start_json] = 0
    h[start_json] = h_func(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict)
    opened_set_queue.put((g[start_json] + h[start_json], puzzle))
    opened_set.add(start_json)
    opened_set_len = 1
    prev_state[start_json] = []
    prev_direction[start_json] = ""
    selected_states = 0
    maximum_states = 0
    while opened_set_queue:
        maximum_states = max(opened_set_len + closed_set_len, maximum_states)
        current_f, current_state = opened_set_queue.get()
        current_state_json = json.dumps(current_state)
        if current_state == solved_puzzle:
            print(h[current_state_json])
            return prev_state, selected_states, maximum_states
        if current_state_json in closed_set:
            continue
        opened_set.remove(current_state_json)
        opened_set_len -= 1
        closed_set.add(current_state_json)
        closed_set_len += 1
        selected_states += 1
        for state, direction in expand(current_state, puzzle_size, prev_direction[current_state_json]):
            state_json = json.dumps(state)
            if not state_json in opened_set and not state_json in closed_set:
                g[state_json] = g[current_state_json] + 1
                h[state_json] = h_update_func(state, solved_puzzle, solved_puzzle_dict, h[current_state_json], direction)
                opened_set_queue.put((g[state_json] + h[state_json], state))
                opened_set.add(state_json)
                opened_set_len += 1
                prev_state[state_json] = current_state
                prev_direction[state_json] = direction
            elif g[state_json] > g[current_state_json] + 1:
                 g[state_json] = g[current_state_json] + 1
                 prev_state[state_json] = current_state
                 prev_direction[state_json] = direction
                 if state_json in opened_set:
                    opened_set_queue.put((g[state_json] + h[state_json], state))
                 else:
                    opened_set_queue.put((g[state_json] + h[state_json], state))
                    opened_set.add(state_json)
                    opened_set_len += 1
                    closed_set.remove(state_json)
                    closed_set_len -= 1
    return None