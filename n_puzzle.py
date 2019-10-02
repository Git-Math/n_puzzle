import sys
import os
import getopt
import copy
import json
import time

import error
import puzzle_generator
import solve

NORMAL_SEARCH = 0
GREEDY_SEARCH = 1
UNIFORM_COST_SEARCH = 2

def usage():
    print("usage: %s [--help] [-p <puzzle_file>|-r <size>] [-i iterations] [-h manhattan|euclidian|hamming|boost] [-g|-u] [-c] [-m]\n\
--help: display this help\n\
-p <puzzle_file>: read puzzle from <puzzle_file>\n\
-r <size>: generate random puzzle of size <size> (default with size 3)\n\
-i <iterations>: number of shuffle iterations for random puzzle (default 10000)\n\
-h <heuristic>: heuristic function (default manhattan)\n\
-g: greedy search\n\
-u: uniform cost search\n\
-c: classic mode\n\
-m: mute" % sys.argv[0])

def print_puzzle(puzzle, puzzle_size):
    max_str_length = len(str(puzzle_size ** 2 - 1))
    for row in puzzle:
        for i, e in enumerate(row):
            print(str(e).rjust(max_str_length), end = "")
            if i < puzzle_size - 1:
                print(" ", end = "")
        print("")

def solved_puzzle(puzzle_size):
    puzzle = [[0 for i in range(puzzle_size)] for i in range(puzzle_size)]
    x = 0
    y = 0
    i_x = 1
    i_y = 0
    for i in range(1, puzzle_size ** 2):
        puzzle[y][x] = i
        if x + i_x < 0 or x + i_x >= puzzle_size or (i_x != 0 and puzzle[y][x + i_x] != 0):
            i_y = i_x
            i_x = 0
        elif y + i_y < 0 or y + i_y >= puzzle_size or (i_y != 0 and puzzle[y + i_y][x] != 0):
            i_x = -i_y
            i_y = 0
        x += i_x
        y += i_y
    return puzzle

def classic_solved_puzzle(puzzle_size):
    puzzle = [[0 for i in range(puzzle_size)] for i in range(puzzle_size)]
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            puzzle[y][x] = x + y * puzzle_size + 1
    puzzle[puzzle_size - 1][puzzle_size - 1] = 0
    return puzzle

def solved_puzzle_dict(solved_puzzle, puzzle_size):
    solved_puzzle_dict = {}
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            solved_puzzle_dict[solved_puzzle[y][x]] = (x, y)
    return solved_puzzle_dict

def find_square(puzzle, square):
    for y, row in enumerate(puzzle):
        for x, s in enumerate(row):
            if s == square:
                return x, y
    error.error("Invalid puzzle")

def find_empty_square(puzzle):
    return find_square(puzzle, 0)

def is_solvable(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict):
    transpositions = 0
    empty_transpositions = 0
    x_empty, y_empty = find_empty_square(puzzle)
    x_empty_solved, y_empty_solved = solved_puzzle_dict[0]
    empty_transpositions = abs(x_empty - x_empty_solved) + abs(y_empty + y_empty_solved)
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            if puzzle[y][x] != solved_puzzle[y][x]:
                x_solved, y_solved = find_square(puzzle, solved_puzzle[y][x])
                puzzle[y][x], puzzle[y_solved][x_solved] = puzzle[y_solved][x_solved], puzzle[y][x]
                transpositions += 1
    return transpositions % 2 == empty_transpositions % 2

def read_puzzle_file(puzzle_filename):
    if not os.path.isfile(puzzle_filename):
        error.error('no such file: %s' % puzzle_filename)
    puzzle = []
    puzzle_size = 0
    try:
        puzzle_file = open(puzzle_filename, "r")
    except:
        error.error("Open puzzle file failed")
    for line in puzzle_file:
        if line[0] == "#":
            continue
        line = line.split("#")[0]
        if puzzle_size == 0:
            try:
                puzzle_size = int(line)
            except:
                puzzle_file.close()
                error.error("Puzzle file: puzzle size must be a number between 2 and 99")
        else:
            try:
                puzzle.append([int(x) for x in line.split()])
            except:
                puzzle_file.close()
                error.error("Puzzle file: invalid line value")
            if len(puzzle[-1]) != puzzle_size:
                puzzle_file.close()
                error.error("Puzzle file: invalid line size")
    puzzle_file.close()
    if len(puzzle) != puzzle_size:
        error.error("Puzzle file: invalid line number")
    return puzzle, puzzle_size

def get_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:r:i:h:gucm", ["help"])
    except getopt.GetoptError as err:
        print(str(err), file=sys.stderr)
        usage()
        sys.exit(1)
    if args != []:
        print("Invalid argument: \"" + str(args[0]) + "\"", file=sys.stderr)
        usage()
        sys.exit(1)
    puzzle = None
    puzzle_size = 0
    heuristic = "manhattan"
    search = NORMAL_SEARCH
    iterations = 10000
    classic = False
    mute = False
    for opt, arg in opts:
        if opt == "--help":
            usage()
            sys.exit()
        elif opt == "-p":
            if puzzle_size != 0:
                print("There can only be one option -p OR one option -r", file=sys.stderr)
                usage()
                sys.exit(1)
            puzzle, puzzle_size = read_puzzle_file(arg)
        elif opt == "-r":
            if puzzle_size != 0:
                print("There can only be one option -p OR one option -r", file=sys.stderr)
                usage()
                sys.exit(1)
            try:
                puzzle_size = int(arg)
                if puzzle_size < 2 or puzzle_size > 99:
                    raise
            except:
                print("-r <size> must be a number between 2 and 99", file=sys.stderr)
                usage()
                sys.exit(1)
        elif opt == "-i":
            try:
                iterations = int(arg)
                if iterations < 0 or iterations > 100000:
                    raise
            except:
                print("-i <iterations> must be a number between 0 and 100 000", file=sys.stderr)
                usage()
                sys.exit(1)
        elif opt == "-h":
            heuristic = arg
            if heuristic != "manhattan" and heuristic != "euclidian" and heuristic != "hamming" and heuristic != "boost":
                usage()
                sys.exit(1)
        elif opt == "-g":
            search = GREEDY_SEARCH
        elif opt == "-u":
            search = UNIFORM_COST_SEARCH
        elif opt == "-c":
            classic = True
        elif opt == "-m":
            mute = True
        else:
            usage()
            sys.exit(1)
    if puzzle == None:
        if puzzle_size == 0:
            puzzle_size = 3
        puzzle = puzzle_generator.generate_puzzle(puzzle_size, iterations, True, classic)
    return puzzle, puzzle_size, heuristic, search, iterations, classic, mute

def print_solution(state, prev_state, puzzle_size, mute):
    state_json = json.dumps(state)
    if prev_state[state_json]:
        move_number = print_solution(prev_state[state_json], prev_state, puzzle_size, mute)
        if not mute:
            print_puzzle(state, puzzle_size)
            print()
        return move_number + 1
    if not mute:
        print_puzzle(state, puzzle_size)
        print()
    return 0

if __name__ == '__main__':
    start_time = time.time()
    puzzle, puzzle_size, heuristic, search, iterations, classic, mute = get_args()
    solved_puzzle = solved_puzzle(puzzle_size) if not classic else classic_solved_puzzle(puzzle_size)
    solved_puzzle_dict = solved_puzzle_dict(solved_puzzle, puzzle_size)
    if not is_solvable(copy.deepcopy(puzzle), puzzle_size, solved_puzzle, solved_puzzle_dict):
        print("Unsolvable puzzle")
        exit()
    try:
        prev_state, selected_states, maximum_states = solve.solve_puzzle(puzzle, puzzle_size, solved_puzzle, solved_puzzle_dict, heuristic, search)
    except:
        error.error("solve_puzzle() failed")
    end_time = time.time()
    move_number = print_solution(solved_puzzle, prev_state, puzzle_size, mute)
    print("Total number of states ever selected in the opened set: %d" % selected_states)
    print("Maximum number of states ever represented in memory at the same time: %d" % maximum_states)
    print("Number of moves required to transition from the initial state to the final state: %d" % move_number)
    print("Time: %.2fs" % (end_time - start_time))
