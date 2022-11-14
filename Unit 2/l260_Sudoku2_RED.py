#Oviya Jeyaprakash 10/29/2022
#Advanced Constraint Satisfaction on Sudoku Part 1
#250

import sys
from collections import deque
from time import perf_counter
import random

total_start = perf_counter()
file = sys.argv[1]
#file = "puzzles_3_standard_medium_more.txt"
sudoku_list = []
global_symbols = "123456789ABCDEFGHIJKLMNOPQRSTUV"
global_symbol_list = ""
global_neighbors = {}
global_subblock = []
#global_board_values = {}

with open(file) as f:
    sudoku_list = [line.strip() for line in f]

def create_board_values(line):
    board_dict = {}
    check_indices = []
    for i in range(len(line)): 
        if line[i] != ".":
            board_dict[i] = {line[i]}
            check_indices.append(i)
        else:
            board_dict[i] = {i for i in global_symbol_list}
    return board_dict, check_indices

def set_up(line): #find n, subblock height/width, symbol list
    symbol_list = []
    s_height = s_width = 0
    n = int(len(line) ** 0.5)
    
    check = int(n ** 0.5)
    while s_height == 0:
        if n % check == 0:
            if check < (n // check):
                s_width = n // check
                s_height = check
            else:
                s_width = check
                s_height = n // check
        check -= 1

    symbol_list = global_symbols[:n]
    global global_symbol_list
    global_symbol_list = symbol_list

    initial_state = create_board_values(line)

    return n, s_height, s_width, symbol_list, initial_state

def print_puzzle(size, s_height, s_width, state):
    line = ""
    for i in range(len(state)):
        if len(state[i]) == 1:
            line += "".join(state[i])
        else:
            line += "."
        
    print((horizontal := "".join(["-" for j in range(size * 2)])))
    for i in range(size):
        temp = ""
        for k in range(size//s_width):
            temp += (" ").join(line[(s := i * size + s_width * k):s + s_width]) + "|"
        print(temp)
        if (i + 1) % s_height == 0:
            print(horizontal)

def make_neighbors(size, s_height, s_width, line):
    global global_neighbors
    global_neighbors = {}
    
    global global_subblock
    global_subblock = []

    temp_coors = [] #top left coor of every subblock
    r = 0
    while r < size:
        c = 0
        while c < size:
            temp_coors.append((r, c))
            c += s_width
        r += s_height

    for coor in temp_coors: #all indexes in each subblock
        temp_subblock = set()
        r = coor[0]
        for i in range(s_height):
            c = coor[1]
            for j in range(s_width):
                temp_subblock.add(r * size + c)
                c += 1
            r += 1
        global_subblock.append(temp_subblock)

    for i in range(len(line)):
        key = i
        value = set()
        for j in range((i // size) * size, (i // size) * size + size): #row
            if j != i:
                value.add(j)
        for k in range(size):
            if (temp := i % size + k * size) != i:
                value.add(temp) #col
        for l in global_subblock:
            if i in l:
                for m in l:
                    if m != i:
                        value.add(m) #subblock
        global_neighbors[key] = value

def crude_check(line):
    temp_dict = {}
    for x in global_symbols:
        temp_dict[x] = line.count(x)
    return temp_dict

def goal_check(state):
    for i in state.values():
        if len(i) != 1:
            return False
    return True

def most_constrained_var(state, size):
    min_length = size
    #min_index = []
    min_index = 0
    for key, val in state.items():
        if (v := len(val)) < min_length and v != 1:
            min_length = v
            min_index = key
            #min_index.append(key)
    #temp = random.randint(0, len(min_index) - 1)
    return min_index

def forward_looking(state, check_indices):
    already_solved = set()
    solved_indices = check_indices.copy()
   
    while len(solved_indices) > 0: ####
        index = solved_indices.pop()
        symbol = ''.join(state[index])

        for n in global_neighbors[index]:
            temp = state[n].copy()
            if symbol in state[n] and n != index:
                temp.remove(symbol)
                state[n] = temp
                if len(state[n]) == 1 and n not in already_solved:
                    solved_indices.append(n)
                if len(state[n]) == 0:
                    return None
        already_solved.add(index)

    return state

def backtrack_extra(state, size):
    if goal_check(state):
        return state
    var = most_constrained_var(state, size)
    #for temp_var in var:
    for val in state[var]:
        new_state = state.copy()
        new_state[var] = {val}
        #print_puzzle(s[0], s[1], s[2], new_state)
        checked_state = forward_looking(new_state, [var])
        if checked_state is not None:
            result = backtrack_extra(checked_state, size)
            if result is not None:
                return result
    return None

# puzzle = ".6.28.....9.4.7A..8....5.....7..78..4.1.31....25.9.....7.83.2.....A9.4..54.2....8.6....293...136.A.8"
# s = set_up(puzzle)
# print_puzzle(s[0], s[1], s[2], s[4][0])
# make_neighbors(s[0], s[1], s[2], s[4][0])

# result = forward_looking(s[4][0], s[4][1])
# #print(result)
# print_puzzle(s[0], s[1], s[2], result)
# result = backtrack_extra(result, s[0])
# #print(result)
# print_puzzle(s[0], s[1], s[2], result)

count = 0
for i in sudoku_list:       
    puzzle = i
    s = set_up(puzzle)
    #print_puzzle(s[0], s[1], s[2], puzzle)
    make_neighbors(s[0], s[1], s[2], s[4][0])
    
    result = forward_looking(s[4][0], s[4][1])
    result = backtrack_extra(result, s[0])
    print("Puzzle", count, "solution:", ''.join([''.join(result[i]) for i in range(len(result))]))
    # r = set_up(result)
    # print_puzzle(r[0], r[1], r[2], result)
    # print(crude_check(result))
    count += 1

# print(global_subblock)
# print("\n")
# print(global_neighbors)


