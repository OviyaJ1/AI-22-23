# Oviya Jeyaprakash, 3/23/2023 
# Tetris and Genetic Algorithms
# l630

from operator import index
from time import perf_counter
import sys
import re
import random
import math
import string
from turtle import clear

POPULATION_SIZE = 500
NUM_CLONES = 20
TOURNAMENT_SIZE = 30
TOURNAMENT_WIN_PROBABILITY = 0.75
#CROSSOVER_LOCATIONS = 2
MUTATION_RATE = 0.2

#input_board = sys.argv[1]
#input_board = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"
empty_line = "          "
full_line  = "##########"

COLUMNS = 10
ROWS = 20

pieces_list = ["I", "O", "T", "S", "Z", "J", "L"]
piece_string_dict = {
    "I": ["####n", "#n#n#n#n"],
    "T":["###n # n","# n##n# n"," # n###n"," #n##n #n"],
    "S":["## n ##n"," #n##n# n"],
    "Z":[" ##n## n","# n##n #n"],
    "O":["##n##n"],
    "J":["# n# n##n","  #n###n","##n #n #n", "###n#  n"],
    "L":["#  n###n"," #n #n##n", "##n# n# n", "###n  #n"],
       
}

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

def make_random_board():
    columns = []
    for i in range(COLUMNS):
        columns.append(random.randint(0, ROWS))
    
    board = ""
    for block in reversed(range(200)):
        column_index = int(block%COLUMNS)
        if columns[column_index] > block/COLUMNS:
            board += "#"
        else:
            board += " "

    board = check_and_clear(board)[1]
    
    return board

def make_population(population_size, num_heurisitic_variables):
    generation_set = set()
    while len(generation_set) < population_size:
        variable_list = []
        for i in range(num_heurisitic_variables):
            variable_list.append(random.uniform(-1.0, 1.0))
        generation_set.add(tuple(variable_list))

    rank_list = []
    for strategy in generation_set:
        rank_list.append((fitness(strategy, 5), strategy))

    return rank_list

def heuristic(board, strategy):
    #num of empty spaces, average of column heights (kind of redundant), num of columns heights greater or equal to 10
    #num of empty rows, num of full rows, score, num of closed off spaces

    a, b, c, d, e, f = strategy
    result_value = 0

    empty_spaces = 0
    empty_rows = 0
    full_rows = 0
    closed_off_spaces = 0
    score_value = 0
    columns_over_10 = 0

    rows = [board[i:i+10] for i in range(0, len(board), 10)]
    columns_heights = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    if board == "GAME OVER":
        return -10000
    
    for block_index in range(len(board)):
        #empty spaces
        if board[block_index] == " ":
            empty_spaces += 1
        
        #closed off spaces
        row_num = int(block_index/COLUMNS)
        if row_num != 0:
            row_num_temp = row_num
            temp_count = 1
            while row_num_temp != 0:
                if board[block_index - (COLUMNS * temp_count)] == "#" and (row_num == 19 or board[block_index + COLUMNS] == "#"):
                    closed_off_spaces += 1
                row_num_temp -= 1

        #columns_heights
        col_num = int(block_index/ROWS)
        if board[block_index] == "#":
            if columns_heights[col_num] == -1:
                columns_heights[col_num] = 20 - row_num

    #column heights cont
    for col in columns_heights:
        if col >= 10:
            columns_over_10 += 1

    #num empty lines and num full lines
    for r in rows:
        if r == empty_line:
            empty_rows += 1
        if r == full_line:
            full_rows += 1
    
    # print(e, full_rows, score_value)
    # if full_rows > 4:
    #     print_board(board)

    #score
    score_value = score(full_rows)
    
    result_value += a * empty_spaces
    result_value += b * empty_rows
    result_value += c * full_rows
    result_value += d * closed_off_spaces
    result_value += e * score_value
    result_value += f * columns_over_10

    return result_value

def play_game(strategy):
    board = make_random_board()
    points = 0
    while board != "GAME OVER":
        random_piece = random.choice(pieces_list)
        value_list = []
        for subpiece in piece_string_dict[random_piece]:
            for col_num in range((subpiece.index("n") - 1), COLUMNS): 
                poss_board = possible_moves(board, subpiece, col_num)
                poss_value = heuristic(poss_board, strategy)
                value_list.append((poss_value, poss_board))
        value_list = sorted(value_list, reverse=True)
        board = value_list[0][1] #board with highest heuristic
        new_points, new_board = check_and_clear(board)
        points += new_points
        board = new_board
    return points

def fitness(strategy, num_trials):
    game_scores = []
    for i in range(num_trials):
        game_scores.append(play_game(strategy))
    return sum(game_scores)/len(game_scores)

def breed(parent1, parent2):
    num_crossover_locations = random.randint(0, len(parent1) - 1)
    child = []
    copy_indices = set()
    while len(copy_indices) < num_crossover_locations:
        copy_indices.add(random.choice(range(len(parent1))))
    
    for i in range(len(parent1)):
        if i in copy_indices:
            child.append(parent1[i])
        else:
            child.append(parent2[i])

    return child 

def mutate(variable_list):
    random_index = random.randint(0, len(variable_list) - 1)
    variable_list[random_index] = random.uniform(-1.0, 1.0)
    return variable_list

def choose_parent(parent_list, tournament_win_probability):
    for parent in parent_list:
        if random.random() < tournament_win_probability:
            return parent[1]

def selection(generation_set, population_size, num_clones, tournament_size, tournament_win_probability, mutation_rate, generation_num):
    new_generation_set = set()

    #ranking generation
    rank_list = []
    for strategy_pair in generation_set: #strategy_pair consists of strategy_fitness and strategy
        rank_list.append((strategy_pair[0], strategy_pair[1]))
    rank_list = sorted(rank_list, reverse=True)
    print(rank_list)

    for i in range(num_clones):
        new_generation_set.add(tuple(rank_list[i][1]))
    #print(new_generation_set)

    print("ranking generation " + str(generation_num) + " done")

    #tournament
    tournament_set = set()
    while len(tournament_set) < (tournament_size * 2):
        random_index = random.randint(0, len(rank_list) - 1)
        tournament_set.add(rank_list[random_index][1])

    print("tournament done")

    #parents
    parent1_list = []
    for j in range(tournament_size):
        strategy = tournament_set.pop()
        parent1_list.append((fitness(strategy, 5), strategy))
    parent1_list = sorted(parent1_list, reverse=True)
    
    parent2_list = []
    for k in range(tournament_size):
        strategy = tournament_set.pop()
        parent2_list.append((fitness(strategy, 5), strategy))
    parent2_list = sorted(parent2_list, reverse=True)

    print("parents done")

    #breeding and mutations
    while len(new_generation_set) < population_size:
        parent1 = choose_parent(parent1_list, tournament_win_probability)
        parent2 = choose_parent(parent2_list, tournament_win_probability)

        child = breed(parent1, parent2)

        if random.random() < mutation_rate:
            child = mutate(child)

        #print(child)
        new_generation_set.add(tuple(child))

    new_rank_list = []
    for new_strategy in new_generation_set:
        #print(new_strategy)
        new_rank_list.append((fitness(new_strategy, 5), new_strategy))
    
    c = rank_list[0]
    if c[0] >= 50000:
        return c

    print(c)

    print("one done")

    # with open('readme.txt', 'w') as f:
    #     f.write(str(c) + "(" + str(fitness(3, encoded_string, c)) + "):\n" + decoded_string + "\n")
    # print()

    # print("Generation " + str(generation_num) +": " + decoded_string)
    # print()

    return selection(new_rank_list, population_size, num_clones, tournament_size, tournament_win_probability, mutation_rate, generation_num + 1)

#print_board(make_random_board())

new_or_saved = input()
if new_or_saved == "NEW":
    new_generation = make_population(POPULATION_SIZE, 6)
    selection(new_generation, POPULATION_SIZE, NUM_CLONES, TOURNAMENT_SIZE, TOURNAMENT_WIN_PROBABILITY, MUTATION_RATE, 0)
elif new_or_saved == "SAVED":
    #pickle
    print("be better")
else:
    print("oops, try again")

#start_time = perf_counter()
#find_possible_moves_actual(input_board)
#print_board(input_board)
#end_time = perf_counter()
#print("Time taken: " + str(end_time - start_time))