#Oviya Jeyaprakash 09/16/2022
#Bidirectional BFS
#150

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

def BiBFS(board):
    goal = find_goal(board)
    fringe_start = deque()
    visited_start = set()
    fringe_end = deque()
    visited_end = set()
    temp_dict = {}

    fringe_start.append((board, 0))
    visited_start.add(board)
    fringe_end.append((goal, 0))
    visited_end.add(goal)
    temp_dict_start = {board: 0}
    temp_dict_end = {goal: 0}

    while fringe_start:
        v1 = fringe_start.popleft()
        v2 = fringe_end.popleft()

        if v1[0] in visited_end:
            return goal, v1[1] + temp_dict_end[v1[0]]
        if v2[0] in visited_start:
            return goal, v2[1] + temp_dict_start[v2[0]]
        for child in get_children(v1[0]):
            if child not in visited_start:
                temp_dict[child] = v1[0]
                fringe_start.append((child, v1[1] + 1))
                temp_dict_start[child] = v1[1] + 1
                visited_start.add(child)
        for child in get_children(v2[0]):
            if child not in visited_end:
                temp_dict[child] = v2[0]
                fringe_end.append((child, v2[1] + 1))
                temp_dict_end[child] = v2[1] + 1
                visited_end.add(child)
    print("Unsolvable")

#print(BiBFS("FCJDBIAGKLOHME.N"))

#tasks:
#2: FCJDBIAGKLOHME.N, 37 moves
#3: BiBFS runs word ladders about two times faster than BFS
#4: I stored the words in two different dictionaries (one for each side), the child of the word was 
#   the key and the word itself was the value. I used the overlapping word that were in both dictionaries
#   to create the word ladder in the end
#5: As long as we know the start and end goal, BiBFS is more advantageous than BFS because checking 
#   in both directions/sides saves a lot more time

count = 0
for x in line_list:
    size, board = x.split()

    print("Line %s" % count + ":")

    start = perf_counter()
    v = BiBFS(board)
    end = perf_counter()
    board_temp = board[0:] + ","
    print("Bidirectional BFS:", board_temp, v[1], "moves found in", end - start)

    start = perf_counter()
    v = BFS(board)
    end = perf_counter()
    board_temp = board[0:] + ","
    print("BFS:", board_temp, v[1], "moves found in", end - start)

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

total_end = perf_counter()
print("Total time:", total_end - total_start)