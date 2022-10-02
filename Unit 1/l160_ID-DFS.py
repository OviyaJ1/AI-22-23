#Oviya Jeyaprakash 10/01/2022
#Iterative-Deepening DFS
#160

import sys
from collections import deque
from time import perf_counter

total_start = perf_counter()
file = sys.argv[1]
#file = "slide_puzzle_tests.txt"

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

def reverse(temp_dict, goal, state):
    word = goal
    solution_path = [goal]
    while word != state:
        solution_path.append(temp_dict[word])
        word = temp_dict[word]
    return solution_path

def BFS(board):
    fringe = deque()
    visited = set()
    temp_dict = {}

    fringe.append((board, 0))
    visited.add(board)
    goal = find_goal(board)
    while fringe:
        v = fringe.popleft()
        if v[0] == goal:
            #print("Moves: %s" % v[1])
            solution_path = reverse(temp_dict, goal, board)
            return v #, solution_path
        for child in get_children(v[0]):
            if child not in visited:
                temp_dict[child] = v[0]
                fringe.append((child, v[1] + 1))
                visited.add(child)
    print("Unsolvable")

def kDFS(state, k):
    fringe = deque()
    start = (state, 0, set())
    start[2].add(state)
    goal = find_goal(state)
    fringe.append(start)
    while fringe:
        v = fringe.pop()
        if v[0] == goal:
            return v[0], v[1]
        if v[1] < k:
            for child in get_children(v[0]):
                if child not in v[2]:
                    c = v[2].copy()
                    c.add(child)
                    temp = (child, v[1] + 1, c)
                    fringe.append(temp)
    return None

def ID_DFS(state):
    max_depth = 0
    result = None
    while result is None:
        result = kDFS(state, max_depth)
        max_depth += 1
    return result

#print(ID_DFS("AIBCFOGD.EKHMJNL"))
#print(BFS("AIBCFOGD.EKHMJNL"))

count = 0
for x in line_list:
    size, board = 4, x

    start_BFS = perf_counter()
    v = BFS(board)
    end_BFS = perf_counter()
    temp_board = board[0:] + ","
    print("Line %s" % count + ":", temp_board, "BFS -", v[1], "moves found in", end_BFS - start_BFS, "seconds")

    start_ID_DFS = perf_counter()
    v = ID_DFS(board)
    end_ID_DFS = perf_counter()
    temp_board = board[0:] + ","
    print("Line %s" % count + ":", temp_board, "ID-DFS -", v[1], "moves found in", end_ID_DFS - start_ID_DFS, "seconds")

    print("\n")
    count += 1

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

#total_end = perf_counter()
#print("Total time:", total_end - total_start)