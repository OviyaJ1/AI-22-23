#Oviya Jeyaprakash 11/17/2022
#TicTacToe
#310

import sys
from collections import deque
from time import perf_counter
final_boards = []

def print_game(board):
    print(board[0] + board[1] + board[2] + "    " + "012")
    print(board[3] + board[4] + board[5] + "    " + "345")
    print(board[6] + board[7] + board[8] + "    " + "678") 
    print("\n")  

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
    children = {}
    for i in range(len(board)):
        if board[i] == ".":
            new_child = board[0:i] + current_player + board[i+1:]
            children[i] = new_child
    return children

def get_player_moves(board, current_player):
    children = {}
    for i in range(len(board)):
        if board[i] == ".":
            new_child = board[0:i] + current_player + board[i+1:]
            children[i] = new_child
    p = ""
    for key in children:
        p += str(key) + ", "
    p = p[:len(p) - 2]
    print(p)
    return children

def min_step(board, initial_board):
    if (v := game_over(board)) != None:
        final_boards.append(board)
        return v, board, initial_board
    results = []
    for next_board in (get_children(board, "O")).values():
        results.append(max_step(next_board, initial_board))
    return min(results)

def max_step(board, initial_board):
    if (v := game_over(board)) != None:
        final_boards.append(board)
        return v, board, initial_board
    results = []
    for next_board in (get_children(board, "X")).values():
        results.append(min_step(next_board, initial_board))
    return max(results)

def max_move(board):
    results = []
    for index, next_board in (get_children(board, "X")).items():
        results.append(((p := min_step(next_board, next_board)), index))
        if p[0] == -1:
            print("Moving at", index, "results in a loss.")
        elif p[0] == 0:
            print("Moving at", index, "results in a tie.")
        else:
            print("Moving at", index, "results in a win.")
    r = max(results)
    print("\n" + "I chose space", r[1], "\n")
    return r[0][2]

def min_move(board):
    results = []
    for index, next_board in (get_children(board, "O")).items():
        results.append(((p := max_step(next_board, next_board)), index))
        if p[0] == -1:
            print("Moving at", index, "results in a win.")
        elif p[0] == 0:
            print("Moving at", index, "results in a tie.")
        else:
            print("Moving at", index, "results in a loss.")
    r = min(results) 
    print("\n" + "I chose space", r[1], "\n")   
    return r[0][2]

official_board = sys.argv[1]
#official_board = "........."
print("Starting board:")
print_game(official_board)

if official_board == ".........":
    #print("Wanna go first? (Say 'yes' or 'no')")
    answer = input("Should I be X or O? ")
    print("\n")

    if answer == "O":
        human_move = True
        while game_over(official_board) == None:
            if human_move:
                print("Your turn: (Choose from 0 - 8)")
                children = get_player_moves(official_board, "X")
                choice = input("Your choice: ")
                print("\n")
                official_board = children[int(choice)]
                print_game(official_board)
                human_move = False
            else:
                official_board = min_move(official_board)
                print_game(official_board)
                human_move = True
    elif answer == 'X':
        human_move = False
        while game_over(official_board) == None:
            if human_move:
                print("Your turn: (Choose from 0 - 8)")
                children = get_player_moves(official_board, "O")
                choice = input("Your choice: ")
                print("\n")
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
                choice = input("Your choice: ")
                print("\n")
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
                choice = input("Your choice: ")
                print("\n")
                official_board = children[int(choice)]
                print_game(official_board)
                human_move = False
            else:
                official_board = min_move(official_board)
                print_game(official_board)
                human_move = True
if game_over(official_board) == 1:
    print("X wins!")
elif game_over(official_board) == 0:
    print("It's a tie!")
else:
    print("O wins!")
    
# while game_over(official_board) == None:
#     official_board = max_move(official_board)
#     print_game(official_board)
#     official_board = input()
#     print_game(official_board)

#print(max_move("XOX......"))
#print_game("........O")
#print(x_wins)
#print(len(x_wins), len(o_wins), len(five), len(seven), len(nine), len(six), len(eight))

    