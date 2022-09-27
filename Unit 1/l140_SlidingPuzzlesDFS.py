#Oviya Jeyaprakash 09/16/2022
#Sliding Puzzles BFS
#120

import sys
from collections import deque
from time import perf_counter
total_start = perf_counter()
#file = sys.argv[1]
file = "011111111111111"
#file = "010100000000000"

# with open(file) as f:
#     line_list = [line.strip() for line in f]

def swap(board, index1, index2, index3): #original peg location, new location, removed peg
    newBoard = ""
    for i in range(len(board)):
        if i == index1 or i == index3:
            newBoard += "0"
        elif i == index2:
            newBoard += "1"
        else:
            newBoard += board[i]
    #print_puzzle(size, newBoard)
    return newBoard

def print_puzzle(board):
    print("    " + (" ").join(board[0])) 
    print("   " + (" ").join(board[1:3]))
    print("  " + (" ").join(board[3:6]))
    print(" " + (" ").join(board[6:10]))
    print((" ").join(board[10:]))

def find_goal(board):
    return "100000000000000"

def where_index(board, row, column): 
    count = index = 0
    while count != row - 1:
        count += 1
        index += count
    index += column
    return index

def is_empty(board, row, column):
    count = index = 0
    while count != row - 1:
        count += 1
        index += count
    index += column
    #print(row, column, index)
    if board[index - 1] == "0":
        return index
    return -1

def get_children(board):
    size = 5
    row = column = 0
    result = []

    #get row and column from index
    for index in range(len(board)):
        if board[index] == "1": 
            num = index + 1
            count = 1
            row = column = 0
            while num > 0:
                num -= count
                count += 1
            row = count - 1
            column = row + num
            #print(index, row, column)
        
            #check
            if column - 2 > 0 and is_empty(board, row, column - 1) == -1 and (index1 := is_empty(board, row, column - 2)) != -1:
                result.append(swap(board, index, index1 - 1, where_index(board, row, column - 1) - 1))

            if column + 2 < row and is_empty(board, row, column + 1) == -1 and (index1 := is_empty(board, row, column + 2)) != -1:
                result.append(swap(board, index, index1 - 1, where_index(board, row, column + 1) - 1))

            if row + 2 <= size and is_empty(board, row + 1, column) == -1 and (index1 := is_empty(board, row + 2, column)) != -1:
                result.append(swap(board, index, index1 - 1, where_index(board, row + 1, column) - 1))
            
            if row + 2 <= size and is_empty(board, row + 1, column + 1) == -1 and (index1 := is_empty(board, row + 2, column + 2)) != -1:
                result.append(swap(board, index, index1 - 1, where_index(board, row + 1, column + 1) - 1))

            if row - 2 > 0 and column - 2 >= 0 and is_empty(board, row - 1, column - 1) == -1 and (index1 := is_empty(board, row - 2, column - 2)) != -1:
                result.append(swap(board, index, index1 - 1, where_index(board, row - 1, column - 1) - 1))
            
            if row - 2 > 0 and column <= (row - 2) and is_empty(board, row - 1, column) == -1 and (index1 := is_empty(board, row - 2, column)) != -1:
                result.append(swap(board, index, index1 - 1, where_index(board, row - 1, column) - 1))
    
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
            return v, solution_path
        for child in get_children(v[0]):
            if child not in visited:
                temp_dict[child] = v[0]
                fringe.append((child, v[1] + 1))
                visited.add(child)
    print("Unsolvable")

def DFS(board):
    fringe = deque()
    visited = set()
    temp_dict = {}

    fringe.append((board, 0))
    visited.add(board)
    goal = find_goal(board)
    while fringe:
        v = fringe.pop()
        if v[0] == goal:
            #print("Moves: %s" % v[1])
            solution_path = reverse(temp_dict, goal, board)
            return v, solution_path
        for child in get_children(v[0]):
            if child not in visited:
                temp_dict[child] = v[0]
                fringe.append((child, v[1] + 1))
                visited.add(child)
    print("Unsolvable")

#print_puzzle("011111111111111")
#print(BFS(file))

print("BFS:" + "\n")
bfs = BFS(file)
count = 1
for i in reversed(bfs[1]):
    print("Move %s" % count + "\n")
    count += 1
    print_puzzle(i)
    print("\n")

print("DFS:" + "\n")
dfs = DFS(file)
count = 1
for i in reversed(dfs[1]):
    print("Move %s" % count + "\n")
    count += 1
    print_puzzle(i)
    print("\n")

# count = 0
# for x in line_list:
#     size, board = x.split()
#     start = perf_counter()
#     v = BFS(board)
#     end = perf_counter()
#     board = board[0:] + ","
#     print("Line %s" % count + ":", board, v[1], "moves found in", end - start)
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

total_end = perf_counter()
print("Total time:", total_end - total_start)