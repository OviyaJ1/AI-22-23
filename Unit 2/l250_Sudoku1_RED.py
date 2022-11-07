#Oviya Jeyaprakash 10/29/2022
#Advanced Constraint Satisfaction on Sudoku Part 1
#250

import sys
from collections import deque
from time import perf_counter

total_start = perf_counter()
file = sys.argv[1]
# file = "puzzles_1_standard_easy.txt"
sudoku_list = []
global_symbols = "123456789ABCDEFGHIJKLMNOPQRSTUV"
global_symbol_list = ""
global_neighbors = {}
global_subblock = []
#global_board_values = {}

with open(file) as f:
    sudoku_list = [line.strip() for line in f]

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

    # for i in range(len(line)): #set up global board dictionary
    #     global_board_values[i] = None
    #     if line[i] != ".":
    #         global_board_values[i] = line[i]

    return n, s_height, s_width, symbol_list

def create_board_values(line):
    board_values = []
    for i in range(len(line)): 
        board_values[i] = None
        if line[i] != ".":
            board_values[i] = line[i]
    return board_values

def print_puzzle(size, s_height, s_width, line):
    print((horizontal := "".join(["-" for j in range(size * 2)])))
    for i in range(size):
        temp = ""
        for k in range(size//s_width):
            temp += (" ").join(line[(s := i * size + s_width * k):s + s_width]) + "|"
        print(temp)
        if (i + 1) % s_height == 0:
            print(horizontal)

def make_neighbors(size, s_height, s_width, line):
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

def get_sorted_values(line, var):
    result = []
    for i in range(len(global_symbol_list)):
        is_valid = True    
        for j in global_neighbors[var]:
            if line[j] == global_symbol_list[i] and is_valid == True:
                is_valid = False
        if is_valid:
            result.append(global_symbol_list[i])
    return result

def backtrack(line):
    if "." not in line:
        return line
    var = line.index(".")
    for val in get_sorted_values(line, var):
        new_state = line[0:var] + str(val) + line[var+1:]
        print(new_state)
        n = set_up(new_state)
        print_puzzle(n[0], n[1], n[2], new_state)
        input()
        result = backtrack(new_state)
        if result is not None:
            return result
    return None

# puzzle = ".2.1........1.3."
# s = set_up(puzzle)
# print_puzzle(s[0], s[1], s[2], puzzle)
# make_neighbors(s[0], s[1], s[2], puzzle)
    
# result = backtrack(puzzle)
# print(result)
# r = set_up(result)
# print_puzzle(r[0], r[1], r[2], result)

count = 0
for i in sudoku_list:       
    puzzle = i
    s = set_up(puzzle)
    #print_puzzle(s[0], s[1], s[2], puzzle)
    make_neighbors(s[0], s[1], s[2], puzzle)
    
    result = backtrack(puzzle)
    print("Puzzle", count, "solution:", result)
    r = set_up(result)
    # print_puzzle(r[0], r[1], r[2], result)
    # print(crude_check(result))
    count += 1

# print(global_subblock)
# print("\n")
# print(global_neighbors)