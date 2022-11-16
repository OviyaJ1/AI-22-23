#Oviya Jeyaprakash 10/29/2022
#Advanced Constraint Satisfaction on Sudoku Part 1
#250

import sys
from collections import deque
from time import perf_counter
final_boards = []
draws = set()
x_wins = set()
o_wins = set()

def game_over(board):
    for r in range(3):
        if (row := board[r*3:(r*3)+3]) == "OOO" or row == "XXX":
            if row == "OOO":    
                return -1
            return 1
    for c in range(3):
        col = board[c] + board[c+3] + board[c+6]
        if col == "OOO":
            return -1
        if col == "XXX":
            return 1
    if (d1 := board[0] + board[4] + board[8]) == "OOO" or d1 == "XXX":
        if d1 == "OOO":    
            return -1
        return 1
    if (d2 := board[2] + board[4] + board[6]) == "OOO" or d2 == "XXX":
        if d2 == "OOO":    
            return -1
        return 1
    if board.count(".") == 0:
        return 0
    return None

def get_children(board, current_player):
    children = set()
    for i in range(len(board)):
        if board[i] == ".":
            new_child = board[0:i] + current_player + board[i+1:]
            children.add(new_child)
    return children

def min_step(board):
    if (v := game_over(board)) != None:
        global final_boards, draws, x_wins, o_wins
        final_boards.append(board)
        if v == 0:
            draws.add(board)
        if v == 1:
            x_wins.add(board)
        if v == -1:
            o_wins.add(board)
        return v
    results = []
    for next_board in get_children(board, "O"):
        results.append(max_step(next_board))
    return max(results)

def max_step(board):
    if (v := game_over(board)) != None:
        global final_boards, draws, x_wins, o_wins
        final_boards.append(board)
        if v == 0:
            draws.add(board)
        if v == 1:
            x_wins.add(board)
        if v == -1:
            o_wins.add(board)
        return v
    results = []
    for next_board in get_children(board, "X"):
        results.append(min_step(next_board))
    return max(results)

max_step(".........")
print(len(final_boards))
print(len(set(final_boards)))
print(len(draws))

five = []
seven = []
nine = []
six = []
eight = []
for i in x_wins:
    if (c := i.count("X")) == 5:
        nine.append(i)
    elif (c := i.count("X")) == 4:
        seven.append(i)
    elif (c := i.count("X")) == 3:
        five.append(i)

for i in o_wins:
    if (c := i.count("O")) == 4:
        eight.append(i)
    elif (c := i.count("O")) == 3:
        six.append(i) 

#print(x_wins)
print(len(x_wins), len(o_wins), len(five), len(seven), len(nine), len(six), len(eight))

    