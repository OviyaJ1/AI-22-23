#Oviya Jeyaprakash 09/16/2022
#Sliding Puzzles AStar
#180

from re import S
import sys
from heapq import heappush, heappop, heapify
from collections import deque
from time import perf_counter
total_start = perf_counter()

file = sys.argv[1]
#file = "slide_puzzle_tests_2.txt"

with open(file) as f:
    line_list = [line.strip() for line in f]

def swap(board, index1, index2):
    newBoard = ""
    for i in range(len(board)):
        if i == index1:
            newBoard += board[index2]
        elif i == index2:
            newBoard += board[index1]
        else:
            newBoard += board[i]
    #print_puzzle(size, newBoard)
    return newBoard

def print_puzzle(size, board):
    for i in range(size):
        print((" ").join(board[(s := i * size):s + size]))

def find_goal(board):
    sort_board = sorted(board)
    goal_state = sort_board[1:]
    goal_state.append(".")
    return ''.join(goal_state)

def get_children(board):
    #check up, down, left, right; -size, +size, -1, +1
    #queue and set
    result = []

    size = int(len(board) ** 0.5)
    i1 = board.index(".")
    if i1 - size >= 0:
        result.append(swap(board, i1, i1 - size))

    if i1 + size < len(board):
        result.append(swap(board, i1, i1 + size))

    if i1 % size != 0:
        result.append(swap(board, i1, i1 - 1))
    
    if (i1 + 1) % size != 0:
        result.append(swap(board, i1, i1 + 1))

    return result

def is_solvable(size, state):
    #size, board = state.split()
    board = state
    #size = 4
    out_of_order = 0

    blank = board.index(".")
    board = board[:blank] + board[blank + 1:]

    for index in range(len(board)):
        for i in board[index:]:
            if ord(board[index]) > ord(i):
                out_of_order += 1
    
    blank = blank//int(size)
    #print("# of out of order pairs:", out_of_order,"/ Blank row:", blank)
    if int(size)%2 != 0:
        if out_of_order%2 != 0:
            return False
        return True
    else:
        if (out_of_order%2 != 0 and blank%2 == 0) or (out_of_order%2 == 0 and blank%2 != 0):
            return True
        return False

def heuristic(size, state):
    #size, board = state.split()
    #size = int(size)
    board = state
    goal = find_goal(board)
    total = 0
    
    for index in range(len(board)):
        if (curr := board[index]) != ".":
            g_index = goal.index(curr)
            g_row = g_index//size
            row = index//size
            g_col = g_index % size
            col = index % size

            total +=  abs(g_row - row) + abs(g_col - col)
    return total

def a_star(size, state):
    if is_solvable(size, state) == False:
        return "no solution"
    goal = find_goal(state)
    closed = set()
    start = (heuristic(size, state), 0, state)
    fringe = []
    heappush(fringe, start)

    while fringe:
        v = heappop(fringe)
        if v[2] == goal:
            return v[0]
        if v[2] not in closed:
            closed.add(v[2])
            for child in get_children(v[2]):
                if child not in closed:
                    temp = (v[1] + 1 + heuristic(size, child), v[1] + 1, child)
                    heappush(fringe, temp)
    return None
    

count = 0
for x in line_list:
    size, board = x.split()
    size = int(size)
    start = perf_counter()
    v = a_star(size, board)
    end = perf_counter()
    board = board[0:] + ","
    print("Line %s" % count + ":", board, "A* -", v, "in", end - start)
    #print("\n")
    count += 1

