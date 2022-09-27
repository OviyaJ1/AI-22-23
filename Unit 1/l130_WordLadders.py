#Oviya Jeyaprakash 09/20/2022
#Word Ladders
#130

import sys
from collections import deque
from time import perf_counter
dict_start = perf_counter()
#file = sys.argv[1]
#dictionary, file_pairs = "words_06_letters.txt", "puzzles_normal.txt"
dictionary, file_pairs = sys.argv[1], sys.argv[2]
line_list = set()
dict_count = 0
word_pairs = []

with open(dictionary) as f:
    line_list = ({line.strip() for line in f})
    dict_count = len(line_list)

with open(file_pairs) as f:
    word_pairs = ([line.strip() for line in f])

def create_dict(line_list):
    word_dict = {}
    for word in line_list:
        value_list = []
        for i in range(len(word)):
            initial_char = word[i]
            for j in "abcdefghijklmnopqrstuvwxyz":
                if j != initial_char:
                    child = word[:i] + j + word[i+1:]
                    if child in line_list:
                        value_list.append(child)
        word_dict[word] = value_list 
    
    dict_end = perf_counter()
    print("Time to create the data structure was:", dict_end - dict_start, "seconds")
    print("There are", dict_count, "words in this dict.")
    return word_dict

def find_goal(line):
    intial_state, goal_state = line.split()
    return intial_state, goal_state

def get_children(word_dict, word):
    return word_dict[word]

def reverse(temp_dict, goal, state):
    word = goal
    solution_path = [goal]
    while word != state:
        solution_path.append(temp_dict[word])
        word = temp_dict[word]
    return solution_path

def BFS(line):
    state, goal = find_goal(line)
    temp_dict = {}

    fringe = deque()
    visited = set()
    path = [state]
    fringe.append((state, path))
    visited.add(state)

    while fringe:
        v = fringe.popleft()
        if v[0] == goal:
            #print("Moves: %s" % v[1])
            solution_path = reverse(temp_dict, goal, state)
            return solution_path
        for child in get_children(word_dict, v[0]):
            if child not in visited:
                temp_dict[child] = v[0]
                fringe.append((child, path))
                visited.add(child)
    print("No Solution!")

#print(BFS("parked yonder"))

count = 0
word_dict = create_dict(line_list)
print("\n")

for line in word_pairs:    
    puzzle_start = perf_counter()
    print("Line:", count)
    l = BFS(line)

    if l:
        print("Length is:", len(l))
        for i in reversed(l):
            print(i)
    
    print("\n")
    count += 1
puzzle_end = perf_counter()

print("Time to solve all of these puzzles was:", puzzle_end - puzzle_start, "seconds")