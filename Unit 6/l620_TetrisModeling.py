# Oviya Jeyaprakash, 3/14/2023 
# Tetris Modeling
# l620

from operator import index
from time import perf_counter
import sys
import re
import random
import math
import string
from turtle import clear

input_board = sys.argv[1]
#input_board = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
empty_line = "          "
full_line  = "##########"

COLUMNS = 10
ROWS = 20

piece_string_dict = {
    "I": ["####n", "#n#n#n#n"],
    "T":["###n # n","# n##n# n"," # n###n"," #n##n #n"],
    "S":["## n ##n"," #n##n# n"],
    "Z":[" ##n## n","# n##n #n"],
    "O":["##n##n"],
    "J":["# n# n##n","  #n###n","##n #n #n", "###n#  n"],
    "L":["#  n###n"," #n #n##n", "##n# n# n", "###n  #n"],
       
}

# pieces_list = ["I", "O", "T", "S", "Z", "J", "L"]
# pieces_moves_dict = {"I": 2, "O": 1, "T": 4, "S": 2, "Z": 2, "J": 4, "L": 4}
# piece_offset_data = {"I": [[0, 0, 0, 0], [0]], "O": [[0, 0]], "T": [[0, 0, 0], [0, -1], [-1, 0, -1], [-1, 0]], "S": [[0, 0, -1], [-1, 0]], "Z": [[-1, 0, 0], [0, -1]], "J": [[0, 0, 0], [0, -2], [-1, -1, 0], [0, 0]], "L": [[0, 0, 0], [0, 0], [0, -1, -1], [-2, 0]]}
# piece_height_data = {"I": [[1, 1, 1, 1], [4]], "O": [[2, 2]], "T": [[1, 2, 1], [3, 2], [2, 2, 2], [2, 3]], "S": [[1, 2, 2], [3, 2]], "Z": [[2, 2, 1], [2, 3]], "J": [[2, 1, 1], [3, 3], [2, 2, 2], [1, 3]], "L": [[1, 1, 2], [3, 1], [2, 2, 2], [3, 3]]}

# for r in range(len(rows)):
#     if rows[r] == full_line:
#         row_full_dict[r] = True
#     else:
#         row_full_dict[r] = False

def print_board(board):
    if board == "GAME OVER":
        print("GAME OVER")
    else:
        print("=======================")
        for count in range(20):
            print(' '.join(list(("|" + board[count * 10: (count + 1) * 10] + "|"))), " ", count)
        print("=======================")
        print()
        print("  0 1 2 3 4 5 6 7 8 9  ")
        print()

def possible_moves_helper(board, subpiece, col_num, row_num):
    temp_board = board
    temp_row = row_num
    piece_place_index = col_num + (temp_row * COLUMNS)

    for block in subpiece:
        if block == "n": 
            temp_row = temp_row + 1
            piece_place_index = col_num + (temp_row * COLUMNS)
        elif block == "#":
            if board[piece_place_index] == "#":
                return "GAME OVER"
            else:
                temp_board = temp_board[0:piece_place_index] + "#" + temp_board[piece_place_index+1:]
                piece_place_index -= 1
        else:
            piece_place_index -= 1
    return temp_board

def possible_moves(board, subpiece, col_num): #finds first possible row and (and only) possible move for that column/subpiece
    row_num = (ROWS - 1) - (subpiece.count("n") - 1)
    result_board = "GAME OVER"
    while result_board == "GAME OVER" and row_num >= 0:
        result_helper_board = possible_moves_helper(board, subpiece, col_num, row_num)
        if result_helper_board == "GAME OVER":
            row_num -= 1
        else:
            result_board = result_helper_board

    return result_board

def score(clear_rows):
    if clear_rows == 0:
        return 0
    elif clear_rows == 1:
        return 40
    elif clear_rows == 2:
        return 100
    elif clear_rows == 3:
        return 300
    elif clear_rows == 4:
        return 1200

def check_and_clear(board):
    rows = [board[i:i+10] for i in range(0, len(board), 10)]
    clear_rows = []
    new_rows = []
    for r in range(len(rows)):
        if rows[r] == full_line:
            clear_rows.append(r)
            new_rows.append(empty_line)
    
    result_score = score(len(clear_rows))

    for r in range(len(rows)):
        if r not in clear_rows:
            new_rows.append(rows[r])

    result_board = "".join(new_rows)

    return result_score, result_board

def find_possible_moves_actual(board):
    f = open("tetrisout.txt", "w")
    #count = 0

    for piece in piece_string_dict.keys():
        for subpiece in piece_string_dict[piece]:
            for col_num in range((subpiece.index("n") - 1), COLUMNS):
                #count += 1
                new_board = possible_moves(board, subpiece, col_num)
                if new_board != "GAME OVER":
                    new_board = check_and_clear(new_board)[1]
                #print_board(new_board)
                f.write(new_board)
                f.write("\n")
    
    f.close()
    #print(count)

start_time = perf_counter()
find_possible_moves_actual(input_board)
#print_board(input_board)
end_time = perf_counter()
#print("Time taken: " + str(end_time - start_time))