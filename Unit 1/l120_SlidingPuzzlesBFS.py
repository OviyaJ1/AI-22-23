#Oviya Jeyaprakash 09/16/2022
#Sliding Puzzles BFS
#120

import sys
from collections import deque
from time import perf_counter
start = perf_counter()
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

def BFS(board):
    fringe = deque()
    visited = set()
    fringe.append((board, 0))
    visited.add(board)
    while fringe:
        v = fringe.popleft()
        if v[0] == find_goal(board):
            print("Moves: %s" % v[1])
            return v
        for child in get_children(v[0]):
            if child not in visited:
                fringe.append((child, v[1] + 1))
                visited.add(child)
    print("done")

def BFS_brainteaser(board):
    board = find_goal(board)
    fringe = deque()
    visited = set()
    fringe.append((board, 0))
    #visited.add(board)

    brain3 = 0 #count
    #brain4 = 0 #max
    brain4_2 = 0 #count
    brain4_3 = []

    while fringe:
        v = fringe.popleft()
        for child in get_children(v[0]):
            if child not in visited:
                fringe.append((child, v[1] + 1))

                if(v[1] + 1 == 10):
                    brain3 += 1
                
                # if(v[1] + 1 > brain3):
                #     brain4 = v[1] + 1

                if(v[1] + 1 == 31):
                    brain4_2 += 1
                    brain4_3.append(child)

                visited.add(child)
    print(brain3)
    print(brain4_2)
    print(brain4_3)
    return visited
    print("done")

def BFS_brainteaser_helper(board):
    fringe = deque()
    visited = set()
    fringe.append((board, 0))
    visited.add(board)
    while fringe:
        v = fringe.popleft()
        if v[0] == find_goal(board):
            return v[1] #returns moves
        for child in get_children(v[0]):
            if child not in visited:
                fringe.append((child, v[1] + 1))
                visited.add(child)
    print("Not Solvable")


BFS("21345678.")


#brainteasers
#1: 2x2 - 12, 3x3 - 181440
#2: 21345678. (code goes through the entire fringe)
#3: 286
#4: 31, ['8672543.1', '64785.321']
#5: ABCFEJGD.MLHNIKO, 20 moves

# count = 0
# for x in line_list:
#     size, board = x.split()
#     v = BFS(board)
#     end = perf_counter()
#     board = board[0:] + ","
#     print("Line ", count, ":", board, v[1], "moves found in", end - start)
#     count += 1

# count = 0
# for x in line_list:
#     size, board = x.split()
#     #print(size, board)
#     print("Line", count, "start state:")
#     print_puzzle(int(size), board)
#     print("Line", count, "goal state:", find_goal(board))
#     print("Line", count, "children:", get_children(board))
#     count += 1
#     print("\n")

end = perf_counter()
print("Total time:", end - start)