#Oviya Jeyaprakash 11/17/2022
#Othello Modeling
#320

import sys
from collections import deque
from time import perf_counter
directions = [-11, -10, -9, -1, 1, 9, 10, 11]

def nicely_print(board):
    board_rows = [board[x:x + 10] for x in range(0, 100, 10)]
    for row in board_rows:
        print(" ".join(list(row)))

def convert_board_8_to_10(board):
    result = "??????????" + "".join(["?" + str(board[i * 8 :i * 8 + 8]) +"?" for i in range(8)]) + "??????????"
    #nicely_print(result)
    return result

def convert_index_10_to_8(index):
    return ((index//10) - 1) * 8 + ((index%10) - 1)

def convert_index_8_to_10(index):
    return ((index//8) + 1) * 10 + ((index%8) + 1)

def possible_moves(board, token):
    board_10 = convert_board_8_to_10(board)
    opponent = "ox"["xo".index(token)]
    possible_move_list = set()
    for i in range(len(board_10)):
        if board_10[i] == token:
            for dir in directions:
                if board_10[i + dir] == opponent:
                    count = 1
                    while board_10[i + (count * dir)] == opponent:
                        count += 1
                    if board_10[(index2 := i + (count * dir))] == ".":
                        #possible_move_list.append((i, index2, dir))
                        #possible_move_list.add(index2)
                        #print(i, index2, dir)
                        possible_move_list.add(convert_index_10_to_8(index2))
    return possible_move_list

def make_move(board, token, index):
    board_10 = convert_board_8_to_10(board)
    changes = {index}
    index_10 = convert_index_8_to_10(index)
    opponent = "ox"["xo".index(token)]

    for dir in directions:
        if board_10[index_10 + dir] == opponent:
            possible_changes = []
            count = 1
            while board_10[(index2 := index_10 + (count * dir))] == opponent:
                count += 1
                possible_changes.append(convert_index_10_to_8(index2))
            if board_10[index_10 + (count * dir)] == token:
                for p in possible_changes:
                    changes.add(p)
                #print(possible_changes, dir, index)

    result = ""
    for i in range(len(board)):
        if i not in changes:
            result += board[i]
        else:
            result += token

    return result


    