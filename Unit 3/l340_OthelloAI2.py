#Oviya Jeyaprakash 12/10/2022
#Othello AI 2
#340

from distutils.file_util import move_file
from time import perf_counter
import sys
from collections import deque
from time import perf_counter
directions = [-11, -10, -9, -1, 1, 9, 10, 11]

def find_next_move(board, token, depth):
    alpha = -99999
    beta = 99999
    p_moves = possible_moves(board, token)
    opponent = "ox"["xo".index(token)]
    result_moves = []
    for m in p_moves:
        if beta > alpha:
            new_score = minimax(make_move(board, token, m), opponent, depth - 1, alpha, beta)
            
            if token == "x" and new_score > alpha:
                alpha = new_score
            elif token == "o" and new_score < beta:
                beta = new_score

            result_moves.append((new_score, m))

    if token == "x":
        return max(result_moves)[1]
    else:
        return min(result_moves)[1]

    #xxx.xxxxxxooxxxoxxxxoxoxxxxoxoxxxxxoxooxxxxooxoxxxoooxxxxxxxxxxx

def nicely_print_10(board):
    board_rows = [board[x:x + 10] for x in range(0, 100, 10)]
    for row in board_rows:
        print(" ".join(list(row)))

def nicely_print_8(board):
    board_rows = [board[x:x + 8] for x in range(0, 64, 8)]
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

def minimax(board, player, depth, alpha, beta):
    opponent = "ox"["xo".index(player)]
    curr_score = general_score(board)
    moves = possible_moves(board, player)

    if depth == 0 or game_over(board):
        return curr_score

    if len(moves) == 0:
        return minimax(board, opponent, depth - 1, alpha, beta)

    result = []
    for m in moves:
        if beta > alpha:
            new_board = make_move(board, player, m)
            new_score = minimax(new_board, opponent, depth - 1, alpha, beta)

            if player == "x" and new_score > alpha:
                alpha = new_score
            elif player == "o" and new_score < beta:
                beta = new_score

            result.append(new_score)
    
    if player == "x":
        return max(result)
    else:
        return min(result)

# def minimax(board, player, depth):
#     if depth is 0 or game_over():
#         return score(board)
#     for move in possible_moves():
#         new_board = make_move()
#         compute_score by calling minimax(new_board, opponent, depth-1)
#     if there were no moves available:
#         return minimax(board, opponent, depth-1)
#     return min or max of  the scores I computed

def endgame_score(board):
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
            return -35000
        else:
            return 35000

    score = 0
    corners = [0, 7, 56, 63]
    adjacent_corners = [1, 9, 8, 6, 14, 15, 48, 49, 57, 54, 55, 62]
    adjacent_corners_extra = {0:(1,9,8), 7:(6,14,15), 56:(48,49,57), 63:(54,55,62)}
    edges = [2, 3, 4, 5, 16, 24, 32, 40, 23, 31, 39, 47, 58, 59, 60, 61]
    x_possible_moves = possible_moves(board, "x")
    o_possible_moves = possible_moves(board, "o")

    #checks edges
    for i in edges: 
        if board[i] == "x":
            score += 300
        elif board[i] == "o":
            score += -300

    #checks corners
    for i in corners: 
        if board[i] == "x":
            score += 2000
        elif board[i] == "o":
            score += -2000

    #checks spaces adjacent to corners
    for i, corners in adjacent_corners_extra.items(): 
        if board[i] == ".":
            for j in corners:
                if board[j] == "x":
                    score += -650
                elif board[j] == "o":
                    score += 650

    #checks for movability
    score += (len(x_possible_moves) - len(o_possible_moves)) * 20

    #checks tokens
    score += board.count("x") * 30
    score += board.count("o") * -30

    return score

def general_score(board):
    if board.count(".") <= 8:
        return endgame_score(board)

    score = 0
    corners = [0, 7, 56, 63]
    adjacent_corners = [1, 9, 8, 6, 14, 15, 48, 49, 57, 54, 55, 62]
    adjacent_corners_extra = {0:(1,9,8), 7:(6,14,15), 56:(48,49,57), 63:(54,55,62)}
    edges = [2, 3, 4, 5, 16, 24, 32, 40, 23, 31, 39, 47, 58, 59, 60, 61]
    x_possible_moves = possible_moves(board, "x")
    o_possible_moves = possible_moves(board, "o")

    #checks corners
    for i in corners: 
        if board[i] == "x":
            score += 5000
        elif board[i] == "o":
            score += -5000

    #checks spaces adjacent to corners
    for i, corners in adjacent_corners_extra.items(): 
        if board[i] == ".":
            for j in corners:
                if board[j] == "x":
                    score += -750
                elif board[j] == "o":
                    score += 750

    
    #checks edges
    for i in edges: 
        if board[i] == "x":
            score += 400
        elif board[i] == "o":
            score += -400
    

    #checks for movability 
    score += (len(x_possible_moves) - len(o_possible_moves)) * 30

    return score

"""class Strategy():
   #logging = True  # Optional
   def best_strategy(self, board, player, best_move, still_running):
       depth = 1
       for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
           best_move.value = find_next_move(board, player, depth)
           depth += 1"""

board = sys.argv[1]
#board = "xxxxxxxxo.xxoooxxoxoxoxxxxoooooxxxxoooxxxxxxoxoxxxxxxooxxxxxxxox"
#nicely_print_8(board)
player = sys.argv[2]
#player = "x"
depth = 1
for count in range(board.count(".")):
# #for count in range(3):
    print((s := find_next_move(board, player, depth)))
    #nicely_print_8(make_move(board, "x", 37))
    depth += 1

"""results = []
with open("boards_timing.txt") as f:
    for line in f:
        board, token = line.strip().split()
        temp_list = [board, token]
        print(temp_list)
        for count in range(1, 6):
            start = perf_counter()
            find_next_move(board, token, count)
            end = perf_counter()
            temp_list.append(str(end - start))
            print("depth", count)
        print(temp_list)
        print()
        results.append(temp_list)

with open("boards_timing_my_results.csv", "w") as g:
    for l in results:
        g.write(", ".join(l) + "\n")"""
    

    