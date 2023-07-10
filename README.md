# N-puzzle
Implementation of the A* algorithm to solve the N-puzzle.  

You can chose from 4 heuristic functions:
- manhattan
- euclidian
- hamming
- boost

You can also use both greedy search and uniform cost search.

## How to run
```
usage: n_puzzle.py [--help] [-p <puzzle_file>|-r <size>] [-i iterations] [-h manhattan|euclidian|hamming|boost] [-g|-u] [-c] [-m]
--help: display this help
-p <puzzle_file>: read puzzle from <puzzle_file>
-r <size>: generate random puzzle of size <size> (default with size 3)
-i <iterations>: number of shuffle iterations for random puzzle (default 10000)
-h <heuristic>: heuristic function (default manhattan)
-g: greedy search
-u: uniform cost search
-c: classic mode
-m: mute
```

## Example
```
$ python3 n_puzzle.py
0 2 8
7 4 6
1 3 5

2 0 8
7 4 6
1 3 5

2 4 8
7 0 6
1 3 5

2 4 8
7 3 6
1 0 5

2 4 8
7 3 6
1 5 0

2 4 8
7 3 0
1 5 6

2 4 0
7 3 8
1 5 6

2 0 4
7 3 8
1 5 6

2 3 4
7 0 8
1 5 6

2 3 4
7 8 0
1 5 6

2 3 4
7 8 6
1 5 0

2 3 4
7 8 6
1 0 5

2 3 4
7 0 6
1 8 5

2 3 4
0 7 6
1 8 5

2 3 4
1 7 6
0 8 5

2 3 4
1 7 6
8 0 5

2 3 4
1 0 6
8 7 5

2 3 4
1 6 0
8 7 5

2 3 0
1 6 4
8 7 5

2 0 3
1 6 4
8 7 5

0 2 3
1 6 4
8 7 5

1 2 3
0 6 4
8 7 5

1 2 3
8 6 4
0 7 5

1 2 3
8 6 4
7 0 5

1 2 3
8 0 4
7 6 5

Total number of states ever selected in the opened set: 943
Maximum number of states ever represented in memory at the same time: 1504
Number of moves required to transition from the initial state to the final state: 24
Time: 0.040s
```
