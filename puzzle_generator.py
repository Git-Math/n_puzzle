import sys
import getopt
import random

import n_puzzle

def usage():
    print("usage: %s [--help] [-i <iterations>] [-s|-u] [-c] <size>\n\
--help: display this help\n\
-i <iterations>: number of shuffle iterations (default 10000)\n\
-s: generate a solvable puzzle (default)\n\
-u: generate an unsolvable puzzle\n\
-c: generate a classic puzzle\n\
<size>: size of the puzzle" % sys.argv[0])

def shuffle_puzzle(puzzle, puzzle_size, iterations):
    for i in range(iterations):
        possible_move = []
        x_empty, y_empty = n_puzzle.find_empty_square(puzzle)
        if x_empty > 0:
            possible_move.append((x_empty - 1, y_empty))
        if x_empty < puzzle_size - 1:
            possible_move.append((x_empty + 1, y_empty))
        if y_empty > 0:
            possible_move.append((x_empty, y_empty - 1))
        if y_empty < puzzle_size - 1:
            possible_move.append((x_empty, y_empty + 1))
        x, y = random.choice(possible_move)
        puzzle[y_empty][x_empty] = puzzle[y][x]
        puzzle[y][x] = 0
    return puzzle

def generate_puzzle(puzzle_size, iterations, solvable, classic):
    puzzle = n_puzzle.solved_puzzle(puzzle_size) if not classic else n_puzzle.classic_solved_puzzle(puzzle_size)
    puzzle = shuffle_puzzle(puzzle, puzzle_size, iterations)
    if not solvable:
        if puzzle[0][0] == 0 or puzzle[0][1] == 0:
            puzzle[1][0], puzzle[1][1] = puzzle[1][1], puzzle[1][0]
        else:
            puzzle[0][0], puzzle[0][1] = puzzle[0][1], puzzle[0][0]
    return puzzle

def print_generated_puzzle(puzzle, puzzle_size, iterations, solvable, classic):
    max_str_length = len(str(puzzle_size ** 2 - 1))
    print("# Randomly generated %s %spuzzle shuffled with %d iterations" % ("solvable" if solvable else "unsolvable", "" if not classic else "classic ", iterations))
    print(puzzle_size)
    for row in puzzle:
        for i, e in enumerate(row):
            print(str(e).rjust(max_str_length), end = "")
            if i < puzzle_size - 1:
                print(" ", end = "")
        print("")

def get_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:suc", ["help"])
    except getopt.GetoptError as err:
        print(str(err), file=sys.stderr)
        usage()
        sys.exit(1)
    if len(args) != 1:
        print("Invalid argument number")
        usage()
        sys.exit(1)
    try:
        puzzle_size = int(args[0])
        if puzzle_size < 2 or puzzle_size > 99:
            raise
    except:
        print("<size> must be a number between 2 and 99", file=sys.stderr)
        usage()
        sys.exit(1)
    iterations = 10000
    solvable = True
    classic = False
    for opt, arg in opts:
        if opt == "--help":
            usage()
            sys.exit()
        elif opt == "-i":
            try:
                iterations = int(arg)
                if iterations < 0 or iterations > 100000:
                    raise
            except:
                print("-i <iterations> must be a number between 0 and 100 000", file=sys.stderr)
                usage()
                sys.exit(1)
        elif opt == "-s":
            solvable = True
        elif opt == "-u":
            solvable = False
        elif opt == "-c":
            classic = True
        else:
            usage()
            sys.exit(1)
    return puzzle_size, iterations, solvable, classic

if __name__ == '__main__':
    puzzle_size, iterations, solvable, classic = get_args()
    puzzle = generate_puzzle(puzzle_size, iterations, solvable, classic)
    print_generated_puzzle(puzzle, puzzle_size, iterations, solvable, classic)
