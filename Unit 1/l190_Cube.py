#Oviya Jeyaprakash 09/16/2022
#Sliding Puzzles AStar
#180

from re import S
import sys
from heapq import heappush, heappop, heapify
from collections import deque
from time import perf_counter
total_start = perf_counter()

#file = sys.argv[1]
file = "slide_puzzle_tests_2.txt"

# move up: top > back > bottom > front > top
# move left: top > left > bottom > right > top
# goal when cube is completely blue

with open(file) as f:
    line_list = [line.strip() for line in f]

def swap(board, index2, cube):

    new_cube_index = index2
    bottom = ""
    s = -1
    if cube[1] == 0:
        bottom = "."
    else:
        bottom = "@"
    old_value = board[index2]
    if old_value == ".":
        s = 0
    else:
        s = 1

    newBoard = ""
    for i in range(len(board)):
        if i == index2:
            newBoard += bottom
        else:
            newBoard += board[i]
    
    new_cube = (cube[0], s, cube[2], cube[3], cube[4], cube[5])

    return newBoard, new_cube_index, new_cube

def print_puzzle(size, board):
    for i in range(size):
        print((" ").join(board[(s := i * size):s + size]))

def find_goal(state):
    size, board = state.split()
    size = int(size)

def get_children(board, cube_index, cube):
    #move up: top > back > bottom > front > top
    #move down: top < back < bottom < front < top
    #move left: top > left > bottom > right > top
    #move right: top < left < bottom < right < top
    #cube: top, bottom, left, right, front, back

    size = int(len(board) ** 0.5)
    i1 = cube_index
    result = []

    top = cube[0]
    bottom = cube[1]
    left = cube[2]
    right = cube[3]
    front = cube[4]
    back = cube[5]

    if i1 - size >= 0: #move up
        new_cube = (front, back, left, right, bottom, top)
        result.append(swap(board, i1 - size, new_cube))
    if i1 + size < len(board): #move down
        new_cube = (back, front, left, right, top, bottom)
        result.append(swap(board, i1 + size, new_cube))
    if i1 % size != 0: #move left
        new_cube = (right, left, top, bottom, front, back)
        result.append(swap(board, i1 - 1, new_cube))
    if (i1 + 1) % size != 0: #move right
        new_cube = (left, right, bottom, top, front, back)
        result.append(swap(board, i1 + 1, new_cube))

    return result

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