#Oviya Jeyaprakash 11/17/2022
#Othello Modeling
#320

from distutils.file_util import move_file
import sys
from collections import deque
from time import perf_counter
directions = [-11, -10, -9, -1, 1, 9, 10, 11]

def find_next_move(board, token, depth):
    p_moves = possible_moves(board, token)
    opponent = "ox"["xo".index(token)]
    curr_score = score(board)
    result_move = p_moves[0]
    for m in p_moves:
        new_score = min_max(make_move(board, token, m), opponent, depth - 1)
        if token == "x":
            if new_score >= curr_score:
                curr_score = new_score
                result_move = m
        else:
            if new_score <= curr_score:
                curr_score = new_score
                result_move = m
    return result_move

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

def game_over(board):
    x_possible_moves = possible_moves(board, "x")
    o_possible_moves = possible_moves(board, "o")

    if "." not in board or (len(x_possible_moves) == 0 and len(o_possible_moves) == 0):
        return True
    return False

def min_max(board, token, depth):
    opponent = "ox"["xo".index(token)]
    curr_score = score(board)
    moves = possible_moves(board, token)

    if depth == 0 or game_over(board):
        return curr_score
    if len(moves) == 0:
        return min_max(board, opponent, depth - 1)

    max = min = curr_score
    index = m[0]
    for m in moves:
        new_score = min_max(m, opponent, depth - 1)
        if token == "x":
            if new_score > max:
                max = new_score
                index = m
        else:
            if new_score < min:
                min = new_score
                index = m
    return index   

def score(board):
    #checks for victories
    if game_over(board): 
        o_num = x_num = 0

        for char in board:
            if char == "o":
                o_num += 1
            elif char == "x":
                x_num += 1

        if o_num == x_num:
            return 0
        elif o_num > x_num:
            return -1000
        else:
            return 1000

    score = 0
    corners = [0, 7, 56, 63]
    adjacent_corners = [1, 9, 8, 6, 14, 15, 48, 49, 57, 54, 55, 62]
    x_possible_moves = possible_moves(board, "x")
    o_possible_moves = possible_moves(board, "o")

    #checks corners
    for i in corners: 
        if board[i] == "x":
            score += 100
        elif board[i] == "o":
            score += -100

    #checks spaces adjacent to corners
    for i in adjacent_corners: 
        if board[i] == "x":
            score += -50
        elif board[i] == "o":
            score += 50

    #checks for movability
    score = (len(x_possible_moves) - len(o_possible_moves)) * 5 

    return score

class Strategy():
    #logging = True

    def best_strategy(self, board, token, best_move, still_running):
        depth = 1
        for count in range(board.count(".")):
            best_move.value = find_next_move(board, token, depth)
            depth += 1