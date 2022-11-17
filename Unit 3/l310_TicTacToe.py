#Oviya Jeyaprakash 10/29/2022
#Advanced Constraint Satisfaction on Sudoku Part 1
#250

import sys
from collections import deque
from time import perf_counter
final_boards = []

def print_game(board):
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("---------")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("---------")
    print(board[6] + " | " + board[7] + " | " + board[8])    

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

def get_player_moves(board, current_player):
    children = list()
    for i in range(len(board)):
        if board[i] == ".":
            new_child = board[0:i] + current_player + board[i+1:]
            children.append(new_child)
    count = 0
    for c in children:
        print("Move:", count)
        print_game(c)
        print("\n")
        count += 1
    return children

def min_step(board, initial_board):
    if (v := game_over(board)) != None:
        final_boards.append(board)
        return v, board, initial_board
    results = []
    for next_board in get_children(board, "O"):
        results.append(max_step(next_board, initial_board))
    return min(results)

def max_step(board, initial_board):
    if (v := game_over(board)) != None:
        final_boards.append(board)
        return v, board, initial_board
    results = []
    for next_board in get_children(board, "X"):
        results.append(min_step(next_board, initial_board))
    return max(results)

def max_move(board):
    results = []
    for next_board in get_children(board, "X"):
        results.append(min_step(next_board, next_board))
    return (max(results))[2]

def min_move(board):
    results = []
    for next_board in get_children(board, "O"):
        results.append(max_step(next_board, next_board))
    return (min(results))[2]

official_board = "........."
print("Starting board:")
print_game(official_board)
#official_board = sys.argv[1]
if official_board == ".........":
    print("Wanna go first? (Say 'yes' or 'no')")
    answer = input()

    if answer == "yes":
        human_move = True
        while game_over(official_board) == None:
            if human_move:
                print("Your turn: (Choose from 0 - 8)")
                children = get_player_moves(official_board, "X")
                choice = input()
                official_board = children[int(choice)]
                print_game(official_board)
                human_move = False
            else:
                official_board = min_move(official_board)
                print_game(official_board)
                human_move = True
    elif answer == 'no':
        human_move = False
        while game_over(official_board) == None:
            if human_move:
                print("Your turn: (Choose from 0 - 8)")
                children = get_player_moves(official_board, "O")
                choice = input()
                official_board = children[int(choice)]
                print_game(official_board)
                human_move = False
            else:
                official_board = max_move(official_board)
                print_game(official_board)
                human_move = True
    else:
        print("bruh moment")
else:
    if official_board.count("O") == official_board.count("X"):
        human_move = False
        while game_over(official_board) == None:
            if human_move:
                print("Your turn: (Choose from 0 - 8)")
                children = get_player_moves(official_board, "O")
                choice = input()
                official_board = children[int(choice)]
                print_game(official_board)
                human_move = False
            else:
                official_board = max_move(official_board)
                print_game(official_board)
                human_move = True
    else:
        human_move = False
        while game_over(official_board) == None:
            if human_move:
                print("Your turn: (Choose from 0 - 8)")
                children = get_player_moves(official_board, "X")
                choice = input()
                official_board = children[int(choice)]
                print_game(official_board)
                human_move = False
            else:
                official_board = min_move(official_board)
                print_game(official_board)
                human_move = True
    
# while game_over(official_board) == None:
#     official_board = max_move(official_board)
#     print_game(official_board)
#     official_board = input()
#     print_game(official_board)

#print(max_move("XOX......"))
#print_game("........O")
#print(x_wins)
#print(len(x_wins), len(o_wins), len(five), len(seven), len(nine), len(six), len(eight))

    