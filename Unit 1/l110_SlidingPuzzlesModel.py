#Oviya Jeyaprakash 09/13/2022
#Sliding Puzzles Model
#110

import sys
from time import perf_counter
start = perf_counter()
file = sys.argv[1]

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



count = 0
for x in line_list:
    size, board = x.split()
    #print(size, board)
    print("Line", count, "start state:")
    print_puzzle(int(size), board)
    print("Line", count, "goal state:", find_goal(board))
    print("Line", count, "children:", get_children(board))
    count += 1
    print("\n")

end = perf_counter()
print("Total time:", end - start)