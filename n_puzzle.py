import sys
import getopt

import error

NORMAL_SEARCH = 0
GREEDY_SEARCH = 1
UNIFORM_COST_SEARCH = 2

def usage():
    print("%s [-i <file>|-r] [-h manhattan|euclidian|hamming|manhattan+] [-g|-u]" % sys.argv[0])

def read_file(file):
    return 0, 0   

def get_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:r:h:gu", ["help"])
    except getopt.GetoptError as err:
        print(str(err), file=sys.stderr)
        usage()
        sys.exit(1)
    puzzle = None
    puzzle_size = 3
    heuristic = "manhattan"
    search = NORMAL_SEARCH
    for opt, arg in opts:
        if opt == "--help":
            usage()
            sys.exit()
        elif opt == "-i":
            puzzle, puzzle_size = read_file(arg)
        elif opt == "-r":
            try:
                puzzle_size = int(arg)
                if puzzle_size < 2 or puzzle_size > 99:
                    raise
            except:
                error.error("-r argument must be a number between 2 and 99")
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
    return puzzle, puzzle_size, heuristic, search

if __name__ == '__main__':
    puzzle, puzzle_size, heuristic, search = get_args()
    