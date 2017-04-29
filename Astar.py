# Astar.py, April 2017
# Uyen Tran
# SID: 1465908
# Date: Apr 20, 2017

# Based on ItrDFS.py, Ver 0.3, April 11, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
import time
import importlib

# DO NOT CHANGE THIS SECTION
if sys.argv == [''] or len(sys.argv) < 2:
    import EightPuzzleWithHeuristics as Problem
    heuristics = lambda s: Problem.HEURISTICS['h_manhattan'](s)

else:
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)

try:
    if len(sys.argv) == 4:
        initial_data = importlib.import_module(sys.argv[3][:-3]).CREATE_INITIAL_STATE()
    else:
        initial_data = importlib.import_module('puzzle2').CREATE_INITIAL_STATE()
except:
    initial_data = None

print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

# Extra section
Problem.CURRENT_HEURISTICS = heuristics # set CURRENT_HEURISTICS in Problem so that State class can use it
TIMER_START = time.time()


# DO NOT CHANGE THIS SECTION
def runAStar():
    # initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT) + " states examined.")
    print('Run time: ' + str(round(time.time() - TIMER_START, 2)) + 's')
    return path, name


# A star search algorithm
# TODO: finish A star implementation
# I simply use list to store OPEN states and sort it for each while loop
# to make it work as a priority queue. This helps to reduce run time
# when checking whether a state is in OPEN or not.
def AStar(initial_state):
    global COUNT, BACKLINKS

    OPEN = []
    OPEN.append(initial_state)
    CLOSED = []
    BACKLINKS[initial_state] = -1

    while OPEN != []:
        # Stop the iterate if run time exceeds 30 seconds
        if time.time() - TIMER_START > 30:
            print('Run time exceeds 30 seconds.')
            print('Eight puzzle search is aborted...')
            return [], Problem.PROBLEM_NAME

        S = OPEN[0]
        del OPEN[0]
        while S in CLOSED:
            S = OPEN[0]
            del OPEN[0]
        CLOSED.append(S)

        # DO NOT CHANGE THIS SECTION: begining
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end

        # TODO: finish A* implementation
        COUNT += 1
        if (COUNT % 32) == 0:
            print(".", end="")
            if (COUNT % 128) == 0:
                print("COUNT = " + str(COUNT))
                print("len(OPEN)=" + str(len(OPEN)))
                print("len(CLOSED)=" + str(len(CLOSED)))

        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if new_state not in OPEN and new_state not in CLOSED:
                    OPEN.append(new_state)
                    BACKLINKS[new_state] = S

        OPEN.sort()


# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = " + str(len(path) - 1))
    return path


if __name__ == '__main__':
    path, name = runAStar()
