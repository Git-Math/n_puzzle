import sys
import getopt

import error

NORMAL_SEARCH = 0
GREEDY_SEARCH = 1
UNIFORM_COST_SEARCH = 2

def usage():
    print("usage: %s [--help] [-p <puzzle_file>|-r <size>] [-i iterations] [-h manhattan|euclidian|hamming|manhattan+] [-g|-u]\n\
--help: display this help\n\
-p <puzzle_file>: read puzzle from <puzzle_file>\n\
-r <size>: generate random puzzle of size <size> (default with size 3)\n\
-i <iterations>: iterations for random puzzle (default 10000)\n\
-h <heuristic>: heuristic function (default manhattan)\n\
-g: greedy search\n\
-u: uniform cost search" % sys.argv[0])

def read_file(file):
    return 0, 0

def get_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:r:i:h:gu", ["help"])
    except getopt.GetoptError as err:
        print(str(err), file=sys.stderr)
        usage()
        sys.exit(1)
    if args != []:
        print("invalid argument: \"" + str(args[0]) + "\"", file=sys.stderr)
        usage()
        sys.exit(1)
    puzzle = None
    puzzle_size = 3
    heuristic = "manhattan"
    search = NORMAL_SEARCH
    iterations = 10000
    for opt, arg in opts:
        if opt == "--help":
            usage()
            sys.exit()
        elif opt == "-p":
            puzzle, puzzle_size = read_file(arg)
        elif opt == "-r":
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
                if iterations < 0 or iterations > 1000000:
                    raise
            except:
                print("-i <iterations> must be a number between 0 and 1 000 000", file=sys.stderr)
                usage()
                sys.exit(1)
        elif opt == "-h":
            heuristic = arg
            if heuristic != "manhattan" and heuristic != "euclidian" and heuristic != "hamming" and heuristic != "manhattan+":
                usage()
                sys.exit(1)
        elif opt == "-g":
            search = GREEDY_SEARCH
        elif opt == "-u":
            search = UNIFORM_COST_SEARCH
        else:
            usage()
            sys.exit(1)
    return puzzle, puzzle_size, heuristic, search, iterations

if __name__ == '__main__':
    puzzle, puzzle_size, heuristic, search, iterations = get_args()
