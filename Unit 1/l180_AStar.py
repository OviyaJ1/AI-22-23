#Oviya Jeyaprakash 09/16/2022
#Sliding Puzzles AStar
#180

import sys
from collections import deque
from time import perf_counter
total_start = perf_counter()

#file = sys.argv[1]
file = "slide_puzzle_tests.txt"

with open(file) as f:
    line_list = [line.strip() for line in f]

def swap(size, board, index1, index2):
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
        result.append(swap(size, board, i1, i1 - size))

    if i1 + size < len(board):
        result.append(swap(size, board, i1, i1 + size))

    if i1 % size != 0:
        result.append(swap(size, board, i1, i1 - 1))
    
    if (i1 + 1) % size != 0:
        result.append(swap(size, board, i1, i1 + 1))

    return result

def is_solvable(state):
    size, board = state.split()
    out_of_order = 0

    blank = board.index(".")
    board = board[:blank] + board[blank + 1:]

    for index in range(len(board)):
        for i in board[index:]:
            if ord(board[index]) > ord(i):
                out_of_order += 1
    #print("out_of_order: %s" % out_of_order)

    blank = blank//int(size)
    print("# of out of order pairs:", out_of_order,"/ Blank row:", blank)
    if int(size)%2 != 0:
        if out_of_order%2 != 0:
            return False
        return True
    else:
        if (out_of_order%2 != 0 and blank%2 == 0) or (out_of_order%2 == 0 and blank%2 != 0):
            return True
        return False

print("CABD.EFGHIJKLMNO", is_solvable("4 CABD.EFGHIJKLMNO")) 
print("\n")
count = 0
for board in line_list:
    #size, board = x.split()
    start = perf_counter()
    v = is_solvable(board)
    end = perf_counter()
    board = board[0:] + ","
    print("Line %s" % count + ":", board, v, end - start)
    print("\n")
    count += 1

