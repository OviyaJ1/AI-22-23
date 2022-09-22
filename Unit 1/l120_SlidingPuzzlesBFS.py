#Oviya Jeyaprakash 09/16/2022
#Sliding Puzzles BFS
#120

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


#brainteasers
#1: 2x2 - 12, 3x3 - 181440
#2: 21345678. (code goes through the entire fringe)
#3: 286
#4: 8672543.1 - 
#   ['12345678.', '1234567.8', '123456.78', '123.56478', '.23156478', 
#   '2.3156478', '23.156478', '23615.478', '23615847.', '2361584.7', 
#   '236158.47', '236.58147', '2365.8147', '2.6538147', '26.538147', 
#   '26853.147', '26853714.', '2685371.4', '268537.14', '268.37514', 
#   '2683.7514', '2.8367514', '28.367514', '28736.514', '28736451.', 
#   '2873645.1', '287364.51', '287.64351', '.87264351', '8.7264351', 
#   '8672.4351', '8672543.1']
#   64785.321 - 
#   ['12345678.', '1234567.8', '1234.6758', '123.46758', '.23146758', 
#   '2.3146758', '23.146758', '23614.758', '2361.4758', '236.14758', 
#   '.36214758', '3.6214758', '36.214758', '36421.758', '3642.1758', 
#   '3642517.8', '364251.78', '364.51278', '.64351278', '6.4351278', 
#   '6543.1278', '6543712.8', '65437128.', '65437.281', '6543.7281', 
#   '6543872.1', '654387.21', '654.87321', '6548.7321', '6.4857321', 
#   '64.857321', '64785.321']
#   Length: 31
#5: ABCFEJGD.MLHNIKO, 20 moves

count = 0
for x in line_list:
    size, board = x.split()
    start = perf_counter()
    v = BFS(board)
    end = perf_counter()
    board = board[0:] + ","
    print("Line %s" % count + ":", board, v[1], "moves found in", end - start)
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