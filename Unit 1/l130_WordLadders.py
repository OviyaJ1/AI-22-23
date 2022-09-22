#Oviya Jeyaprakash 09/20/2022
#Word Ladders
#130

import sys
from collections import deque
from time import perf_counter
total_start = perf_counter()
#file = sys.argv[1]
file = "words_06_letters.txt"
line_list = set()

with open(file) as f:
    line_list = ({line.strip() for line in f})

def create_dict(line_list):
    word_dict = {}
    for word in line_list:
        value_set = set()
        for i in range(len(word)):
            initial_char = word[i]
            for j in "abcdefghijklmnopqrstuvwxyz":
                if j != initial_char:
                    child = word[:i] + j + word[i+1:]
                    if child in line_list:
                        value_set.add(child)
        word_dict[word] = value_set 
    return word_dict

def find_goal(line):
    intial_state, goal_state = line.split()
    return intial_state, goal_state

def get_children(state):
    result = []
    for i in range(len(state)):
        initial_char = state[i]
        for j in "abcdefghijklmnopqrstuvwxyz":
            if j != initial_char:
                child = state[:i] + j + state[i+1:]
                if child in line_list:
                    result.append(child)
    return result

def deep_copy_path(list):
    new_list = []
    for i in list:
        new_list.append(i)
    return new_list

def BFS(line):
    state, goal = find_goal(line)
    fringe = deque()
    visited = set()
    path = [state]
    fringe.append((state, path))
    visited.add(state)
    while fringe:
        v = fringe.popleft()
        if v[0] == goal:
            #print("Moves: %s" % v[1])
            return v
        for child in get_children(v[0]):
            if child not in visited:
                new_path = deep_copy_path(path)
                new_path.append(child)
                fringe.append((child, new_path))
                visited.add(child)
    print("Unsolvable")

print(BFS("boiler bulled"))